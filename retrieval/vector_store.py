from langchain_chroma import Chroma
from retrieval.embeddings import get_embedding_model
from langchain_community.retrievers import BM25Retriever

def build_vector_store(chunks):

    db = Chroma.from_documents(chunks, get_embedding_model())

    return db

def build_bm25_store(chunks):

    bm25 = BM25Retriever.from_documents(chunks, k=6)

    return bm25