db = None

def set_db(vector_store):
    global db
    db = vector_store


def get_db():
    return db