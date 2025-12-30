from fastapi import FastAPI
from app.api.orders import router as orders_router
from app.api.health import router as health_router

app = FastAPI(
    title="AI Print Estimator",
    description="""
🖨️ **AI-driven print order estimation and intake engine**

### What this system does
• Accepts unstructured print orders (email / WhatsApp / RFQ text)  
• Uses AI to extract print specifications  
• Applies deterministic pricing rules  
• Flags feasibility and turnaround risks  

### Intended users
• Sales teams  
• Customer support (CSR)  
• Print operations teams
""",
    version="1.0.0"
)

app.include_router(orders_router)
app.include_router(health_router)