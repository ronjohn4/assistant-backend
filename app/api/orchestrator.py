# TODO - get tools working with the orchestrator
# TODO - build CI/CD chains for all containers
# TODO - make sure all changes are committed
# TODO - ensure all containers are up to date


from langchain.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Robust import for ChatAnthropic across langchain versions / packages
try:
    from langchain.chat_models import ChatAnthropic
except Exception:
    from langchain_anthropic import ChatAnthropic

from pydantic import BaseModel, Field

from app.api.getdatetime import get_datetime_subagent
from app.api.getweather import get_weather_subagent
from app.api.generalknowledge import get_general_knowledge
from app.config import Config


class Output(BaseModel):
    input: str = Field(description="The original input")
    content: str = Field(description="The content of the response from the LLM")


class Orchestrator:
    """Orchestrator that delegates to sub-agents to fulfill user requests."""



    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]


    def __init__(self):
        self.session = []
        self.store = {}
        self.model = ChatAnthropic(model=Config.ORCHESTRATOR_MODEL, api_key=Config.ANTHROPIC_API_KEY)
        self.tools = [get_weather_subagent, get_datetime_subagent, get_general_knowledge]

        self.orchestrator_agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt="You are a manager. Delegate research to the researcher tools."
        )

        self.orchestrator = RunnableWithMessageHistory(self.model, self._get_session_history,)


    # def ask(self, history: list[tuple[str, str]], query: str) -> Output:
    def ask(self, query: str, history: list[tuple[str, str]]) -> str:
        messages = []
        system = (
            "Categorize user requests as one of the following: "
            "1. Weather related "
            "2. Date or Time related "
            "3. General "
            "If the category is General, answer the question using the get_general_knowledge tool. "
            "Otherwise, delegate to the appropriate sub-agent and return only the sub-agent's response. "
            "Return the category in the response."
        )

        messages.append({"role": "system", "content": system})

        if history:
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})

        messages.append({"role": "user", "content": query})

        # result = self.orchestrator.invoke({"messages": messages})1

        config = {"configurable": {"session_id": "user_session_123"}}
        result = self.orchestrator.invoke(query, config=config)


        # guard for varying result formats
        if isinstance(result, dict) and "messages" in result and len(result["messages"]) > 0:
             content = result["messages"][-1].content
        else:
            # fallback for lower-level return values
            content = str(result)

        # return Output(input=prompt_input, content=content)  # when using the structured Output model
        return content
        