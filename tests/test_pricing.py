"""Tests for the price lookup service."""

import pytest

from services.price_service import PRICE_LIST, get_price


class TestGetPrice:
    def test_returns_price_for_valid_grade_and_size(self):
        assert get_price("60", "12") == PRICE_LIST["60"]["12"]

    def test_grade_80_is_priced_above_grade_60_for_same_size(self):
        """Higher grade steel must never be cheaper than lower grade."""
        for size in PRICE_LIST["60"]:
            assert get_price("80", size) > get_price("60", size)

    def test_size_10_carries_a_premium_over_larger_sizes(self):
        """Small diameter rebar is priced higher in the current list."""
        assert get_price("60", "10") > get_price("60", "12")
        assert get_price("80", "10") > get_price("80", "12")

    @pytest.mark.parametrize(
        "grade,size",
        [
            ("40", "12"),   # unsupported grade
            ("60", "8"),    # unsupported size
            ("60", "40"),   # unsupported size
            ("", ""),       # empty input
        ],
    )
    def test_returns_none_for_unsupported_combinations(self, grade, size):
        assert get_price(grade, size) is None

    def test_all_prices_are_positive(self):
        for grade, sizes in PRICE_LIST.items():
            for size, price in sizes.items():
                assert price > 0, f"grade {grade} size {size} has a non-positive price"

    def test_both_grades_cover_the_same_sizes(self):
        """A size available in one grade should be available in the other."""
        assert set(PRICE_LIST["60"]) == set(PRICE_LIST["80"])