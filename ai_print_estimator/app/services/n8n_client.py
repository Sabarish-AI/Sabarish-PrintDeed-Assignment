import requests
import json
import uuid
import uuid
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

def json_safe(obj):
    # UUID → string
    if isinstance(obj, uuid.UUID):
        return str(obj)

    # datetime → ISO string
    if isinstance(obj, datetime):
        return obj.isoformat()

    # Pydantic models → dict
    if isinstance(obj, BaseModel):
        return obj.dict()

    # Fallback (safe)
    return str(obj)


class N8NClient:
    @staticmethod
    def send_order(order_payload: dict):
        try:
            payload = json.loads(
                json.dumps(order_payload, default=json_safe)
            )

            response = requests.post(
                N8N_WEBHOOK_URL,
                json=payload,
                timeout=5
            )
            response.raise_for_status()

        except Exception as e:
            print("⚠️ n8n webhook error:", e)