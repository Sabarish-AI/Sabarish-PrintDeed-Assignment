from app.services.pricing_engine import calculate_pricing


def test_pricing_basic():
    specs = {
        "quantity": 1000,
        "material_gsm": 170,
        "color_mode": "color",
        "finish": "matte",
        "turnaround_days": 5
    }

    result = calculate_pricing(specs)
    assert result["total_price"] > 0
    assert result["material_cost"] > 0