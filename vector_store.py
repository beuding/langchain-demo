import os
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config import PERSIST_DIR, DOC_FILE, TOP_K

def init_vector_store(embedding):
    if not os.path.exists(PERSIST_DIR):
        loader = TextLoader(DOC_FILE, encoding="utf-8")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n## ", "\n### ", "\n\n", "\n", "。", "，", " "]
        )
        chunks = text_splitter.split_documents(documents)
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=PERSIST_DIR
        )
    else:
        vectordb = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding
        )
    return vectordb

retriever = None

@tool
def search_knowledge(query: str) -> str:
    """检索企业行政制度知识库，包括考勤、休假、差旅报销和离职流程。输入用户问题。"""
    global retriever
    if retriever is None:
        return "知识库尚未初始化。"
    docs = retriever.invoke(query)
    if not docs:
        return "知识库中未找到相关内容。"
    return "\n\n".join([doc.page_content for doc in docs])
