from fastapi import FastAPI
from dotenv import load_dotenv
from loaders.folder_loader import process_folder
from retrieval.vector_store import build_vector_store
from retrieval.db import set_db
from api.routes import router

load_dotenv()

app = FastAPI()

docs = process_folder("test_doc")
db = build_vector_store(docs)
set_db(db)

app.include_router(router)