from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

from assistant.config import OPENAI_API_KEY, LLM
from assistant.agent.tools import search_tool


llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=LLM, temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


researcher = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # choose the agent type that suits your needs
    verbose=True,  # set to True for detailed logs
    memory=memory,  # optional memory component
)
