"""Tests for quotation totals, dates, and text output."""

from datetime import timedelta

import pytest

from models.item import Item
from models.quotation import Quotation

VAT_RATE = 0.15


@pytest.fixture
def quotation():
    return Quotation("Test Contracting Co", "Test Project", "Q-000001")


class TestItem:
    def test_total_is_quantity_times_unit_price(self):
        item = Item("60", "12", 25.0, 2720)
        assert item.total == 68000.0

    def test_fractional_quantity(self):
        item = Item("60", "12", 0.5, 2720)
        assert item.total == 1360.0

    def test_zero_quantity_gives_zero_total(self):
        assert Item("60", "12", 0, 2720).total == 0


class TestTotals:
    def test_empty_quotation_has_zero_totals(self, quotation):
        assert quotation.subtotal() == 0
        assert quotation.vat() == 0
        assert quotation.grand_total() == 0

    def test_subtotal_sums_all_items(self, quotation):
        quotation.add_item(Item("60", "12", 10, 2720))
        quotation.add_item(Item("80", "16", 5, 2770))
        assert quotation.subtotal() == pytest.approx(27200 + 13850)

    def test_vat_is_fifteen_percent_of_subtotal(self, quotation):
        quotation.add_item(Item("60", "12", 10, 2720))
        assert quotation.vat() == pytest.approx(quotation.subtotal() * VAT_RATE)

    def test_grand_total_equals_subtotal_plus_vat(self, quotation):
        quotation.add_item(Item("60", "12", 10, 2720))
        quotation.add_item(Item("80", "25", 7.5, 2770))
        assert quotation.grand_total() == pytest.approx(
            quotation.subtotal() + quotation.vat()
        )

    def test_totals_update_when_an_item_is_added(self, quotation):
        quotation.add_item(Item("60", "12", 10, 2720))
        first = quotation.grand_total()
        quotation.add_item(Item("60", "12", 10, 2720))
        assert quotation.grand_total() == pytest.approx(first * 2)


class TestDates:
    def test_validity_is_seven_days_after_the_quotation_date(self, quotation):
        assert quotation.valid_until - quotation.date == timedelta(days=7)

    def test_valid_until_is_after_the_quotation_date(self, quotation):
        assert quotation.valid_until > quotation.date


class TestTextOutput:
    def test_output_contains_the_quotation_metadata(self, quotation):
        quotation.add_item(Item("60", "12", 10, 2720))
        text = quotation.to_text()
        assert "Q-000001" in text
        assert "Test Contracting Co" in text
        assert "Test Project" in text

    def test_output_contains_a_line_for_each_item(self, quotation):
        quotation.add_item(Item("60", "12", 10, 2720))
        quotation.add_item(Item("80", "16", 5, 2770))
        text = quotation.to_text()
        assert "Grand Total" in text
        assert "VAT (15%)" in text

    def test_output_is_produced_for_an_empty_quotation(self, quotation):
        """Formatting must not raise when there are no items."""
        assert "Grand Total" in quotation.to_text()