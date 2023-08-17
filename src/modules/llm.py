from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

ChatGPT = ChatOpenAI(model="gpt-3.5-turbo",  temperature=0, openai_api_key='temp')
ChatGPT = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, openai_api_key='temp')
Embedding = OpenAIEmbeddings(openai_api_key='temp')

# print(ChatGPT.generate('你好'))
tools = [CurrentStockPriceTool(), StockPerformanceTool()]

agent = initialize_agent(tools, llm=ChatGPT, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)