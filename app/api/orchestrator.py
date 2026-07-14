# TODO - get tools working with the orchestrator
# TODO - handle deprecated langchain calls
# TODO - use the system prompt

from langchain.messages import HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# Robust import for ChatAnthropic across langchain versions / packages
try:
    from langchain.chat_models import ChatAnthropic
except Exception:
    from langchain_anthropic import ChatAnthropic

from pydantic import BaseModel, Field
from typing import Annotated
from typing_extensions import TypedDict

from app.api.getdatetime import get_datetime_subagent
from app.api.getweather import get_weather_subagent
from app.api.generalknowledge import get_general_knowledge
from app.config import Config


class Output(BaseModel):
    input: str = Field(description="The original input")
    content: str = Field(description="The content of the response from the LLM")


class GraphState(TypedDict):
    messages: Annotated[list, add_messages]


class Orchestrator:
    """Orchestrator that delegates to sub-agents to fulfill user requests."""

    def __init__(self):
        system_prompt = (
            "Categorize user requests as one of the following: "
            "1. Weather related "
            "2. Date or Time related "
            "3. General "
            "If the category is General, answer the question using the get_general_knowledge tool. "
            "Otherwise, delegate to the appropriate sub-agent and return only the sub-agent's response. "
            "Answer with short, to the point responses."
        )
       
        workflow = StateGraph(GraphState)
        workflow.add_node("agent", self._call_model)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
        self.model = ChatAnthropic(
            model=Config.ORCHESTRATOR_MODEL, 
            api_key=Config.ANTHROPIC_API_KEY
        )
        self.tools = [get_weather_subagent, get_datetime_subagent, get_general_knowledge]


    def _call_model(self, state: GraphState):
        response = self.model.invoke(state["messages"])
        return {"messages": [response]}
    

    def ask(self, query: str) -> str:
        config = {"configurable": {"thread_id": "conversation-session-123"}}
        input_message = HumanMessage(content=query)
        result = self.app.invoke({"messages": [input_message]}, config)
        content = result["messages"][-1].content
        return content
        