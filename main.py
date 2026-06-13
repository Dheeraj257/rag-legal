from fastapi import FastAPI
from dotenv import load_dotenv
from retrieval.vector_store import load_bm25_store, load_vector_store
from retrieval.db import set_db, set_bm25
from api.routes import router

load_dotenv()

app = FastAPI()

db = load_vector_store("./chroma_db")
bm25 = load_bm25_store("bm25_index.pkl")
set_db(db)
set_bm25(bm25)

app.include_router(router)