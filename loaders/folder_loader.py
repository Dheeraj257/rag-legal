from pathlib import Path
from loaders.csv_loader import load_csv
from loaders.pdf_loader import load_pdf
from loaders.word_loader import load_doc
from chunking.chunker import chunk_documents

def process_folder(file_path):

    folder = Path(file_path)
    all_chunks = []
    files = 0
    failed = 0

    
    for file in folder.iterdir():
        try:
            if file.suffix == ".pdf":
                doc_load = load_pdf(file)
                chunk = chunk_documents(doc_load, "legal")
            elif file.suffix == ".docx":
                doc_load = load_doc(file)
                chunk = chunk_documents(doc_load, "legal")
            elif file.suffix == ".csv":
                doc_load = load_csv(file)
                chunk = chunk_documents(doc_load, "csv")
            else:
                continue
            
            all_chunks.extend(chunk)
            files += 1
            print(f"Processed {Path(file_path).name}, total {files}")
        except Exception as e:
            print(f"Failed: {file.name} — {e}")
            failed += 1

    print(f"\nTotal: {files} files, {len(all_chunks)} chunks, {failed} failed")
    return all_chunks