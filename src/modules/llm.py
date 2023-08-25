import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

import config

__import__('utils.init')
openai.proxy = config.proxy
ChatGPT = ChatOpenAI(model="gpt-3.5-turbo",  temperature=0.7, openai_api_key='temp')
ChatGPT0613 = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, openai_api_key='temp')
Embedding = OpenAIEmbeddings(model= "text-embedding-ada-002", openai_api_key='temp')
