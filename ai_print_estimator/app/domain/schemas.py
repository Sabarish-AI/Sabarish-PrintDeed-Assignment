from pydantic import BaseModel, Field
from typing import Optional, List
from app.domain.enums import Severity


class OrderInput(BaseModel):
    message: str = Field(
        description="Unstructured print order text (email, chat, RFQ)"
    )


class PrintSpecs(BaseModel):
    product: Optional[str] = Field(description="Type of print product")
    quantity: Optional[int] = Field(description="Number of copies")
    size: Optional[str] = Field(description="Paper size (A4, A3, etc.)")
    width_mm: Optional[int] = Field(description="Custom width (mm)")
    height_mm: Optional[int] = Field(description="Custom height (mm)")
    material_gsm: Optional[int] = Field(description="Paper thickness (GSM)")
    color_mode: Optional[str] = Field(description="Color or black & white")
    finish: Optional[str] = Field(description="Surface finish")
    turnaround_days: Optional[int] = Field(description="Delivery time in days")


class PricingResult(BaseModel):
    material_cost: float = Field(description="Paper/material cost")
    print_cost: float = Field(description="Printing cost")
    finishing_cost: float = Field(description="Lamination or coating cost")
    rush_fee: float = Field(description="Urgent delivery surcharge")
    margin: float = Field(description="Business margin")
    total_price: float = Field(description="Final estimated price")


class ValidationIssue(BaseModel):
    issue: str = Field(description="Validation or risk message")
    severity: Severity = Field(description="Risk severity level")


class MarketComparison(BaseModel):
    position: str = Field(
        description="below_market | within_market | above_market | unavailable"
    )
    market_min: Optional[float] = None
    market_max: Optional[float] = None
    currency: Optional[str] = None
    sources: Optional[List[str]] = None
    message: Optional[str] = None


class EstimationResponse(BaseModel):
    specs: PrintSpecs
    pricing: PricingResult
    validations: List[ValidationIssue]
    market_comparison: MarketComparison