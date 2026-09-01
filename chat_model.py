from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

def get_llm(temperature: float = 0.1):
    llm = ChatTongyi(
        model="qwen-turbo",
        temperature=temperature,
    )
    return llm

def get_embedding():
    embedding = DashScopeEmbeddings(
        model="text-embedding-v2"
    )
    return embedding
