db = None
bm25 = None

def set_db(vector_store):
    global db
    db = vector_store


def get_db():
    return db


def set_bm25(bm25_retriever):
    global bm25
    bm25 = bm25_retriever 


def get_bm25():
    return bm25