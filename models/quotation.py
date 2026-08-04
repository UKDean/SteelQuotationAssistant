from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from models.item import Item

QUOTATIONS_DIRECTORY = Path("quotations")


class Quotation:
    """Represents a quotation containing customer, project, and item data."""

    @staticmethod
    def get_next_number() -> int:
        """Calculate the next quotation sequence number from saved text files."""
        if not QUOTATIONS_DIRECTORY.exists():
            return 1

        files = [
            file for file in QUOTATIONS_DIRECTORY.iterdir()
            if file.suffix == ".txt"
        ]
        return len(files) + 1

    def __init__(self, customer_name: str, project_name: str, number: str | None = None):
        self.number = number or f"Q-{Quotation.get_next_number():06d}"
        self.date = datetime.now()
        self.valid_until = self.date + timedelta(days=7)
        self.customer_name = customer_name
        self.project_name = project_name
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add an item line to the quotation."""
        self.items.append(item)

    def subtotal(self) -> float:
        """Return the total price before VAT."""
        return sum(item.total for item in self.items)

    def vat(self) -> float:
        """Return the VAT amount for the quotation."""
        return self.subtotal() * 0.15

    def grand_total(self) -> float:
        """Return the quotation total including VAT."""
        return self.subtotal() + self.vat()

    def _build_header(self) -> str:
        return (
            "============================================================\n"
            "                    AL RAJHI STEEL\n"
            "============================================================\n\n"
            f"Quotation No : {self.number}\n"
            f"Date         : {self.date.strftime('%d-%b-%Y')}\n"
            f"Valid Until  : {self.valid_until.strftime('%d-%b-%Y')}\n\n"
            f"Customer     : {self.customer_name}\n"
            f"Project      : {self.project_name}\n\n"
            f"{'Grade':<8}"
            f"{'Size':<8}"
            f"{'Qty':>10}"
            f"{'Unit Price':>18}"
            f"{'Total':>18}\n" +
            "-" * 62 + "\n"
        )

    def _build_items(self) -> str:
        lines = []
        for item in self.items:
            lines.append(
                f"{item.grade:<8}"
                f"{item.size:<8}"
                f"{item.quantity:>10.2f}"
                f"{item.unit_price:>18,.2f}"
                f"{item.total:>18,.2f}"
            )
        return "\n".join(lines)

    def _build_totals(self) -> str:
        return (
            "\n" + "-" * 62 + "\n"
            f"Subtotal   : {self.subtotal():,.2f} SAR\n"
            f"VAT (15%)  : {self.vat():,.2f} SAR\n"
            f"Grand Total: {self.grand_total():,.2f} SAR\n\n"
            "============================================================"
        )

    def to_text(self) -> str:
        """Return the full quotation content as plain text."""
        return self._build_header() + self._build_items() + self._build_totals()
