import pandas as pd
from pathlib import Path
from langchain_core.documents import Document

def load_csv(file_path):

    csv_doc = []
    file_name = Path(file_path).name

    df = pd.read_csv(file_path)

    for idx, row in df.iterrows():
        content = "\n".join([
            f"{col}: {row[col]}"
            for col in df.columns]
        )

        csv_doc.append(Document(
            page_content=content,
            metadata={
                "source": file_name,
                "citation": f"{file_name}: {idx+2}"
            }
        ))

    return csv_doc

