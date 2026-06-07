import fitz
from pathlib import Path
from langchain_core.documents import Document as LCDocument
from PIL import Image, ImageEnhance
import pytesseract
import io

def extract_text_page(page):

    texts = []

    blocks = page.get_text("blocks")

    for block in blocks:
        x0, y0, x1, y1, content, _, block_type = block
        if block_type == 0:
            text = content.strip()
            texts.append({
                "content": text,
                "y_pos": y0
            })
    
    return texts

def extract_ocr_page(image):

    image = image.convert("L")

    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(2.0)

    sharpness_enhancer = ImageEnhance.Sharpness(image)
    image = sharpness_enhancer.enhance(2.0)

    ocr_text = pytesseract.image_to_string(
        image,
        config= "--psm 3 --oem 1")
    
    return ocr_text


def load_pdf(file_path):

    file_name = Path(file_path).name
    pdf_docs = []

    with fitz.open(file_path) as pdf:

        for page_num, page in enumerate(pdf.pages(),start=1):

            elements = []
            text = extract_text_page(page)
            for block in text:
                elements.append({
                    "content": block["content"],
                    "y_pos": block["y_pos"],
                    "type": "text"
                })


            for img_ref in page.get_images(full=True):
                xref = img_ref[0]
                bbox = page.get_image_bbox(img_ref)
                base_image = pdf.extract_image(xref)
                pil_image = Image.open(io.BytesIO(base_image["image"]))
                ocr_text = extract_ocr_page(pil_image)
                elements.append({
                    "content": ocr_text,
                    "y_pos": bbox.y0,
                    "type": "image"
                })

            elements.sort(key=lambda x:x["y_pos"])

            for element in elements:
                if len(element["content"]) < 20:
                    continue
                pdf_docs.append(LCDocument(
                    page_content=element["content"],
                    metadata={
                        "source": file_name,
                        "page": page_num,
                        "type": element["type"]
                    }
                ))
  
    return pdf_docs

