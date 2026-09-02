"""Tests for persistence and quotation numbering."""

import database
from models.item import Item
from models.quotation import Quotation


class TestSchema:
    def test_create_database_is_idempotent(self, temp_database):
        """Running the app twice must not fail or duplicate tables."""
        database.create_database()
        database.create_database()

    def test_expected_tables_exist(self, temp_database):
        with database.get_connection() as connection:
            rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        names = {row[0] for row in rows}
        assert {"customers", "projects", "quotations", "quotation_items"} <= names


class TestNumbering:
    def test_first_number_on_an_empty_database(self, temp_database):
        assert database.get_next_quotation_number() == "Q-000001"

    def test_number_increments_after_a_quotation_is_saved(self, temp_database):
        quotation = Quotation("Customer", "Project", "Q-000001")
        quotation.add_item(Item("60", "12", 10, 2720))
        customer_id = database.save_customer(quotation.customer_name)
        project_id = database.save_project(customer_id, quotation.project_name)
        database.save_quotation(customer_id, project_id, quotation)

        assert database.get_next_quotation_number() == "Q-000002"

    def test_numbers_are_zero_padded_to_six_digits(self, temp_database):
        number = database.get_next_quotation_number()
        assert number.startswith("Q-")
        assert len(number) == 8


class TestPersistence:
    def test_saved_quotation_keeps_its_totals(self, temp_database):
        quotation = Quotation("Customer", "Project", "Q-000001")
        quotation.add_item(Item("60", "12", 10, 2720))
        quotation.add_item(Item("80", "16", 5, 2770))

        customer_id = database.save_customer(quotation.customer_name)
        project_id = database.save_project(customer_id, quotation.project_name)
        quotation_id = database.save_quotation(customer_id, project_id, quotation)
        database.save_items(quotation_id, quotation.items)

        with database.get_connection() as connection:
            row = connection.execute(
                "SELECT subtotal, vat, grand_total FROM quotations WHERE id = ?",
                (quotation_id,),
            ).fetchone()

        assert row[0] == quotation.subtotal()
        assert row[1] == quotation.vat()
        assert row[2] == quotation.grand_total()

    def test_all_items_are_saved(self, temp_database):
        quotation = Quotation("Customer", "Project", "Q-000001")
        quotation.add_item(Item("60", "12", 10, 2720))
        quotation.add_item(Item("80", "16", 5, 2770))
        quotation.add_item(Item("60", "25", 3, 2720))

        customer_id = database.save_customer(quotation.customer_name)
        project_id = database.save_project(customer_id, quotation.project_name)
        quotation_id = database.save_quotation(customer_id, project_id, quotation)
        database.save_items(quotation_id, quotation.items)

        with database.get_connection() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM quotation_items WHERE quotation_id = ?",
                (quotation_id,),
            ).fetchone()[0]

        assert count == 3

    def test_project_is_linked_to_its_customer(self, temp_database):
        customer_id = database.save_customer("Customer")
        project_id = database.save_project(customer_id, "Project")

        with database.get_connection() as connection:
            row = connection.execute(
                "SELECT customer_id FROM projects WHERE id = ?", (project_id,)
            ).fetchone()

        assert row[0] == customer_id