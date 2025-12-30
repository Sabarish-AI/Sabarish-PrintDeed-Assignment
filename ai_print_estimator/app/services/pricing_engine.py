"""
Deterministic pricing engine for print estimation.
This module MUST NOT use AI.
"""

PRICING_RULES = {
    "material_cost_per_gsm_unit": 0.002,
    "color_print_cost": 2.0,
    "bw_print_cost": 1.0,
    "finish_cost": {
        "matte": 500.0,
        "gloss": 600.0,
        "none": 0.0
    },
    "rush_multiplier": 0.25,
    "margin": 0.30
}


def calculate_pricing(specs: dict) -> dict:
    """
    Calculate print pricing based on extracted specs.
    """

    quantity = specs.get("quantity") or 0
    material_gsm = specs.get("material_gsm") or 0
    color_mode = specs.get("color_mode", "color")
    finish = specs.get("finish", "none")
    turnaround_days = specs.get("turnaround_days")

    material_cost = quantity * material_gsm * PRICING_RULES["material_cost_per_gsm_unit"]

    print_cost = quantity * (
        PRICING_RULES["color_print_cost"]
        if color_mode == "color"
        else PRICING_RULES["bw_print_cost"]
    )

    finishing_cost = PRICING_RULES["finish_cost"].get(finish, 0.0)

    subtotal = material_cost + print_cost + finishing_cost

    rush_fee = (
        subtotal * PRICING_RULES["rush_multiplier"]
        if turnaround_days is not None and turnaround_days < 4
        else 0.0
    )

    margin = subtotal * PRICING_RULES["margin"]

    return {
        "material_cost": round(material_cost, 2),
        "print_cost": round(print_cost, 2),
        "finishing_cost": round(finishing_cost, 2),
        "rush_fee": round(rush_fee, 2),
        "margin": round(margin, 2),
        "total_price": round(subtotal + rush_fee + margin, 2)
    }