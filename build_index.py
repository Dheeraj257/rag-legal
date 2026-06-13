from loaders.folder_loader import process_folder
from retrieval.vector_store import build_bm25_store, build_vector_store


docs = process_folder("test_doc")
build_vector_store(docs)
build_bm25_store(docs)

print("Index built and saved successfully")