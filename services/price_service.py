from typing import Dict, Optional

PRICE_LIST: Dict[str, Dict[str, int]] = {
    "60": {
        "10": 2880,
        "12": 2720,
        "14": 2720,
        "16": 2720,
        "18": 2720,
        "20": 2720,
        "25": 2720,
        "32": 2720,
    },
    "80": {
        "10": 2930,
        "12": 2770,
        "14": 2770,
        "16": 2770,
        "18": 2770,
        "20": 2770,
        "25": 2770,
        "32": 2770,
    },
}


def get_price(grade: str, size: str) -> Optional[int]:
    """Return the unit price for a specific grade and size."""
    return PRICE_LIST.get(grade, {}).get(size)
