import re

STANDARD_SIZES = ["A0", "A1", "A2", "A3", "A4", "A5", "A6"]


def normalize_size(raw_text: str, extracted_size: str | None) -> str | None:
    # If LLM already extracted size, trust it
    if extracted_size:
        return extracted_size

    text = raw_text.upper()

    for size in STANDARD_SIZES:
        if re.search(rf"\b{size}\b", text):
            return size

    return None