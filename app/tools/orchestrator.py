# TODO - handle deprecated langchain calls

from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage, AIMessage

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
from app.config import Config


class GraphState(TypedDict):
    messages: Annotated[BaseMessage, add_messages]


class Orchestrator:
    """Orchestrator that delegates to sub-agents to fulfill user requests."""

    def bot(self, state: GraphState):
        config = {"configurable": {"thread_id": "conversation-session-123"}}
        # response = self.app.invoke(state["messages"], config=config)
        # response = self.model.invoke(state["messages"], config=config)


        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
        response = self.llm_with_tools.invoke(messages, config=config)
        return {"messages": [response]}
    
    def __init__(self):
        self.system_prompt = (
            "Determine if a tool cal is required to respond to the query.  If so, call the tool." \
            "If no tool call is required, form a general response to the query." \
            "Always use the shortest response possible while answering the question directly."
        )
        self.tools = [get_datetime_tool, get_weather_tool, web_search_tool]

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
        if Config.LOG_LEVEL == 'DEBUG':
            png_data = self.app.get_graph().draw_mermaid_png()
            with open("langgraph_graph.png", "wb") as f:
                f.write(png_data)

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
