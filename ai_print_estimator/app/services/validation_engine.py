from typing import List
from app.domain.schemas import ValidationIssue
from app.domain.enums import Severity


def validate_specs(specs: dict) -> List[ValidationIssue]:
    issues = []

    if not specs.get("quantity"):
        issues.append(
            ValidationIssue(
                issue="Quantity is missing",
                severity=Severity.HIGH
            )
        )

    if not specs.get("size"):
        issues.append(
            ValidationIssue(
                issue="Print size not specified",
                severity=Severity.MEDIUM
            )
        )

    if specs.get("turnaround_days") is not None and specs["turnaround_days"] <= 2:
        issues.append(
            ValidationIssue(
                issue="Rush order may impact feasibility",
                severity=Severity.LOW
            )
        )

    return issues