from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.schemas import OrderInput, EstimationResponse
from app.repositories.order_repo import OrderRepository
from app.services.spec_normalizer import normalize_size
from app.services.llm_extractor import extract_specs
from app.services.pricing_engine import calculate_pricing
from app.services.validation_engine import validate_specs
from app.services.competitor_pricing import benchmark_price
from app.services.n8n_client import N8NClient

router = APIRouter(prefix="/orders", tags=["Orders"])


# ==========================================================
# HELPER – BUILD N8N WORKFLOW PAYLOAD
# ==========================================================
def build_n8n_payload(order, specs, pricing, validations, benchmark, input_type):
    return {
        "order_id": order.id,
        "specs": specs,
        "pricing": pricing,
        "validations": validations,
        "market_comparison": benchmark,
        "workflow": {
            "status": "pending_csr_review",
            "current_stage": "csr_review",
            "allowed_actions": ["approve", "reject", "escalate"]
        },
        "meta": {
            "source": "ai_print_estimator",
            "input_type": input_type,
            "confidence": 0.93,
            "version": "1.0.0"
        }
    }


# ==========================================================
# TEXT-ONLY ENDPOINT
# ==========================================================
@router.post(
    "/text",
    response_model=EstimationResponse,
    summary="Estimate print order from free text",
    description="""
Paste a customer order (email / chat / RFQ text).

The system will:
• Extract print specs using AI  
• Calculate pricing using business rules  
• Validate feasibility  
• Compare with market benchmarks  
• Trigger CSR workflow via n8n
"""
)
def create_order_from_text(
    payload: OrderInput,
    db: Session = Depends(get_db)
):
    # Save raw order
    order = OrderRepository.create(db, payload.message, "text")

    # AI + rules
    specs = extract_specs(payload.message)
    pricing = calculate_pricing(specs)
    validations = validate_specs(specs)
    benchmark = benchmark_price(pricing, specs)

    # 🔔 Send to n8n (async orchestration)
    n8n_payload = build_n8n_payload(
        order=order,
        specs=specs,
        pricing=pricing,
        validations=validations,
        benchmark=benchmark,
        input_type="text"
    )
    N8NClient.send_order(n8n_payload)

    return {
        "specs": specs,
        "pricing": pricing,
        "validations": validations,
        "market_comparison": benchmark
    }


# ==========================================================
# UNIFIED INTAKE ENDPOINT (TEXT / EMAIL / PDF / IMAGE)
# ==========================================================
@router.post(
    "/intake",
    response_model=EstimationResponse,
    summary="Unified intake for text, email, PDF, or image",
    description="""
Accepts:
• Text input  
• Email subject + body  
• PDF RFQs  
• Image uploads (scanned orders)

All inputs are normalized into text before AI processing.
Triggers CSR workflow via n8n.
"""
)
async def intake_order(
    text: str | None = Form(default=None),
    email_subject: str | None = Form(default=None),
    email_body: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db)
):
    # ------------------------------------------------------
    # NORMALIZE INPUT → RAW TEXT
    # ------------------------------------------------------
    if text:
        raw_text = text
        input_type = "text"

    elif email_subject or email_body:
        raw_text = f"{email_subject or ''}\n{email_body or ''}".strip()
        input_type = "email"

    elif file:
        file_bytes = await file.read()
        filename = file.filename.lower()
        input_type = "file"

        if filename.endswith(".pdf"):
            from app.utils.pdf_parser import extract_text_from_pdf
            raw_text = extract_text_from_pdf(file_bytes)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            from app.utils.image_ocr import extract_text_from_image
            raw_text = extract_text_from_image(file_bytes)

        else:
            raise HTTPException(
                status_code=415,
                detail="Unsupported file type"
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="No valid input provided"
        )

    # ------------------------------------------------------
    # PROCESS ORDER
    # ------------------------------------------------------
    order = OrderRepository.create(db, raw_text, input_type)

    specs = extract_specs(raw_text)
    specs["size"] = normalize_size(raw_text, specs.get("size"))

    if not any(v is not None for v in specs.values()):
        raise HTTPException(
            status_code=422,
            detail="Unable to extract print specifications. Manual review required."
        )

    pricing = calculate_pricing(specs)
    validations = validate_specs(specs)
    benchmark = benchmark_price(pricing, specs)

    # 🔔 Send to n8n
    n8n_payload = build_n8n_payload(
        order=order,
        specs=specs,
        pricing=pricing,
        validations=validations,
        benchmark=benchmark,
        input_type=input_type
    )
    N8NClient.send_order(n8n_payload)

    return {
        "specs": specs,
        "pricing": pricing,
        "validations": validations,
        "market_comparison": benchmark
    }