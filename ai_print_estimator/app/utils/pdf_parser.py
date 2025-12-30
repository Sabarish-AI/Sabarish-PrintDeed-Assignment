import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text().strip()
            if page_text:
                text.append(page_text)
    return "\n".join(text)