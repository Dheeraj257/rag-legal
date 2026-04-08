from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(doc, doc_type: str="general"):

    if doc_type == "legal":
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=150, separators=["\n\n","\n","; ",". "," ",""])
        chunks = splitter.split_documents(doc)
        return chunks
    elif doc_type == "csv":
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0, separators=["\n"])
        chunks = splitter.split_documents(doc)
        return chunks
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, separators=["\n\n","\n","; ",". "," ",""])
        chunks = splitter.split_documents(doc)
        return chunks
    