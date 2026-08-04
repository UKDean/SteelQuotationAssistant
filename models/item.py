from dataclasses import dataclass


@dataclass
class Item:
    """Represents a single item line in a quotation."""

    grade: str
    size: str
    quantity: float
    unit_price: float

    @property
    def total(self) -> float:
        """Calculate the total price for this item."""
        return self.quantity * self.unit_price
