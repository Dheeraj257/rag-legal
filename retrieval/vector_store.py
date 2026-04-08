from langchain_chroma import Chroma
from retrieval.embeddings import get_embedding_model

def build_vector_store(chunks):

    db = Chroma.from_documents(chunks, get_embedding_model())

    return db

