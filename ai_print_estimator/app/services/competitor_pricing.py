import csv
from pathlib import Path
from typing import Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RATE_CARD_PATH = BASE_DIR / "data" / "print_rates.csv"


# =========================================================
# LOAD NORMALIZED RATE CARD
# =========================================================
def load_rate_card():
    rows = []
    with open(RATE_CARD_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "category": row["category"].lower(),
                "size": row["size"].upper(),
                "gsm_min": int(row["material_gsm_min"]),
                "gsm_max": int(row["material_gsm_max"]),
                "qty_min": int(row["qty_min"]),
                "qty_max": int(row["qty_max"]),
                "rate_min": float(row["rate_min"]),
                "rate_max": float(row["rate_max"]),
            })
    return rows


RATE_CARD = load_rate_card()


# =========================================================
# BENCHMARK LOGIC
# =========================================================
def benchmark_price(pricing: Dict, specs: Dict) -> Dict:
    quantity = specs.get("quantity")
    product = specs.get("product")
    size = specs.get("size")
    gsm = specs.get("material_gsm")

    if not all([quantity, product, size, gsm]):
        return _unavailable("missing_specs")

    total_price = pricing.get("total_price", 0)
    if total_price <= 0:
        return _unavailable("invalid_price")

    our_unit_price = total_price / quantity

    matched = [
        r for r in RATE_CARD
        if r["category"] == product.lower()
        and r["size"] == size.upper()
        and r["gsm_min"] <= gsm <= r["gsm_max"]
        and r["qty_min"] <= quantity <= r["qty_max"]
    ]

    if not matched:
        return _unavailable("no_matching_slab")

    market_min = min(r["rate_min"] for r in matched)
    market_max = max(r["rate_max"] for r in matched)

    if our_unit_price < market_min:
        position = "below_market"
    elif our_unit_price > market_max:
        position = "above_market"
    else:
        position = "within_market"

    return {
        "position": position,
        "market_min": round(market_min, 2),
        "market_max": round(market_max, 2),
        "currency": "INR",
        "sources": ["internal_rate_card"],
    }


def _unavailable(reason: Optional[str] = None):
    return {
        "position": "unavailable",
        "market_min": None,
        "market_max": None,
        "currency": None,
        "sources": ["internal_rate_card"],
    }