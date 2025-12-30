from fastapi import UploadFile
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.image_ocr import extract_text_from_image

def extract_text_from_input(
    text: str | None,
    email_subject: str | None,
    email_body: str | None,
    file: UploadFile | None
) -> str | None:

    if text:
        return text

    if email_subject or email_body:
        return f"{email_subject or ''}\n{email_body or ''}".strip()

    if file:
        content_type = file.content_type

        if content_type == "application/pdf":
            return extract_text_from_pdf(file)

        if content_type.startswith("image/"):
            return extract_text_from_image(file)

    return None