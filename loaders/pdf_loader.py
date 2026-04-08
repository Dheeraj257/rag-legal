import fitz
from pathlib import Path
from langchain_core.documents import Document as LCDocument


def load_pdf(file_path):

    file_name = Path(file_path).name
    pdf_docs = []

    with fitz.open(file_path) as pdf:

        for page_num, page in enumerate(pdf.pages()):

            text = pdf.get_page_text(page_num)

            if len(text) < 20:
                continue

            pdf_docs.append(LCDocument(
                page_content=text,
                metadata={
                    "source": file_name,
                    "page": page_num,
                    "citation": f"{file_name}: {page_num}"
                }
            ))

    return pdf_docs


