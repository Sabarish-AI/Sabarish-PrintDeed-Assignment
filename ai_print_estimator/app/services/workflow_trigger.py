import httpx
from app.config import settings


async def trigger_n8n_workflow(payload: dict):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            settings.N8N_WEBHOOK_URL,
            json=payload
        )
        response.raise_for_status()
        return response.json()