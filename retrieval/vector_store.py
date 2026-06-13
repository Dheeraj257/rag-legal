from langchain_chroma import Chroma
from retrieval.embeddings import get_embedding_model
from langchain_community.retrievers import BM25Retriever
import pickle

def build_vector_store(chunks):

    db = Chroma.from_documents(chunks, 
                               get_embedding_model(),
                               persist_directory="./chroma_db")

def load_vector_store(path):

    loaded_db = Chroma(
        persist_directory=path,
        embedding_function=get_embedding_model()
    )

    return loaded_db

def build_bm25_store(chunks):

    bm25 = BM25Retriever.from_documents(chunks, k=6)
    pickle.dump(bm25, open("bm25_index.pkl","wb"))

def load_bm25_store(path):

    with open(path, "rb") as f:
        loaded_bm25 = pickle.load(f)

        return loaded_bm25
