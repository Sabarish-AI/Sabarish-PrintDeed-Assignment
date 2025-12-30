from enum import Enum


class OrderStatus(str, Enum):
    RECEIVED = "received"
    ESTIMATED = "estimated"
    VALIDATION_FAILED = "validation_failed"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"