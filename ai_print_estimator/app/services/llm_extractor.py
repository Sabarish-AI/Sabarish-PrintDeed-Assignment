import json
import re
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

PROMPT = """
You are a professional print production estimator.

Extract structured data from the order text.
If a value is missing, return null.

Return ONLY valid JSON. Do not add explanations.

Schema:
{
  "product": "brochure|poster|flyer|banner",
  "quantity": number | null,
  "size": "A4|A3|A2|custom" | null,
  "width_mm": number | null,
  "height_mm": number | null,
  "material_gsm": number | null,
  "color_mode": "bw|color",
  "finish": "matte|gloss|none",
  "turnaround_days": number | null
}

Order:
"""

def _safe_json_extract(text: str) -> dict:
    """
    Extract JSON even if wrapped in text or markdown.
    """
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM output: {text}")

    return json.loads(match.group())


@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
def extract_specs(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You output ONLY JSON."},
            {"role": "user", "content": PROMPT + text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return _safe_json_extract(content)
    except Exception as e:
        raise RuntimeError(
            f"LLM JSON parse failed. Raw output: {content}"
        ) from e