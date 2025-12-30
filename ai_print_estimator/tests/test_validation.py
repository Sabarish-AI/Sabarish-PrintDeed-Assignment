from app.services.validation_engine import validate_specs
from app.domain.enums import Severity


def test_missing_quantity():
    specs = {"material_gsm": 170}
    issues = validate_specs(specs)

    assert len(issues) == 1
    assert issues[0]["severity"] == Severity.HIGH