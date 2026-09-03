# TODO - handle deprecated langchain calls

from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage, AIMessage
from pathlib import Path

# Robust import for ChatAnthropic across langchain versions / packages
try:
    from langchain.chat_models import ChatAnthropic
except Exception:
    from langchain_anthropic import ChatAnthropic

from typing import Annotated
from typing_extensions import TypedDict

from app.tools.getdatetimetool import get_datetime_tool
from app.tools.getweathertool import get_weather_tool
from app.tools.websearchtool import web_search_tool
from app.tools.mydatatool import mydata_tool
from app.tools.obsidiantool import search_obsidian_notes
from app.tools.filemanagementtool import init_file_management_tools
# from app.tools.gmailtool import init_gmail_tools

from app.config import Config


class GraphState(TypedDict):
    messages: Annotated[BaseMessage, add_messages]


class Orchestrator:
    """Orchestrator that delegates to sub-agents to fulfill user requests."""
    
    def __init__(self):
        prompt_path = Path("assistant_working_dir/orchestrator_prompt.txt")
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        fm_tools = init_file_management_tools() 
        # gmail_tools = init_gmail_tools()
        # self.tools = [get_datetime_tool, get_weather_tool, web_search_tool, mydata_tool, search_obsidian_notes] + fm_tools + gmail_tools
        self.tools = [get_datetime_tool, get_weather_tool, web_search_tool, mydata_tool, search_obsidian_notes] + fm_tools

        workflow = StateGraph(GraphState)
        workflow.add_node("agent", self.bot)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_edge('tools', 'agent')
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)
        workflow.add_conditional_edges("agent", self.should_continue)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
        self.model = ChatAnthropic(
            model=Config.ORCHESTRATOR_MODEL, 
            api_key=Config.ANTHROPIC_API_KEY
        )
        self.llm_with_tools = self.model.bind_tools(self.tools)

        # Create an image of the workflow graph for debugging
        # if Config.LOG_LEVEL == 'DEBUG':
        #     png_data = self.app.get_graph().draw_mermaid_png()
        #     with open("langgraph_graph.png", "wb") as f:
        #         f.write(png_data)

    def bot(self, state: GraphState):
        # reload system_prompt just in case it was updated
        prompt_path = Path("assistant_working_dir/orchestrator_prompt.txt")
        self.system_prompt = prompt_path.read_text(encoding="utf-8")
        
        # config is used when the same bot and graph is handling multiple conversations
        config = {"configurable": {"thread_id": "conversation-session-123"}}
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
        response = self.llm_with_tools.invoke(messages, config=config)
        return {"messages": [response]}
    
    def should_continue(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM made a tool call, route to the tools node
        if last_message.tool_calls:
            return "tools"
        return END

    def ask(self, query: str) -> str:
        config = {"configurable": {"thread_id": "conversation-session-123"}}
        user_input = {"messages": [
            ("user", query)
        ]}
        response = self.app.invoke(user_input, config=config)
        return response["messages"][-1].text
