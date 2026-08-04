import sqlite3
from pathlib import Path
from typing import Iterable

DB_FOLDER = Path("data")
DB_NAME = "steel.db"
DB_PATH = DB_FOLDER / DB_NAME


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection for the project database."""
    return sqlite3.connect(DB_PATH)


def _ensure_database_folder() -> None:
    """Ensure the database folder exists before connecting."""
    DB_FOLDER.mkdir(parents=True, exist_ok=True)


def _execute_script(script: str) -> None:
    """Execute a SQL script against the database."""
    _ensure_database_folder()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.executescript(script)


def create_database() -> None:
    """Create the SQLite database and required tables."""
    _execute_script(
        """
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            project_name TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        );

        CREATE TABLE IF NOT EXISTS quotations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quotation_no TEXT,
            quotation_date TEXT,
            valid_until TEXT,
            customer_id INTEGER,
            project_id INTEGER,
            subtotal REAL,
            vat REAL,
            grand_total REAL,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(project_id) REFERENCES projects(id)
        );

        CREATE TABLE IF NOT EXISTS quotation_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quotation_id INTEGER,
            grade TEXT,
            size TEXT,
            quantity REAL,
            unit_price REAL,
            total REAL,
            FOREIGN KEY(quotation_id) REFERENCES quotations(id)
        );
        """
    )


def save_customer(name: str) -> int:
    """Save a new customer and return its database id."""
    _ensure_database_folder()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO customers(name) VALUES (?)",
            (name,),
        )
        return cursor.lastrowid


def save_project(customer_id: int, project_name: str) -> int:
    """Save a new project and return its database id."""
    _ensure_database_folder()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO projects(customer_id, project_name) VALUES (?, ?)",
            (customer_id, project_name),
        )
        return cursor.lastrowid


def save_quotation(customer_id: int, project_id: int, quotation) -> int:
    """Save a quotation record and return its database id."""
    _ensure_database_folder()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO quotations(
                quotation_no,
                quotation_date,
                valid_until,
                customer_id,
                project_id,
                subtotal,
                vat,
                grand_total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                quotation.number,
                quotation.date.strftime("%Y-%m-%d"),
                quotation.valid_until.strftime("%Y-%m-%d"),
                customer_id,
                project_id,
                quotation.subtotal(),
                quotation.vat(),
                quotation.grand_total(),
            ),
        )
        return cursor.lastrowid


def get_next_quotation_number() -> str:
    """Return the next unique quotation number based on database state."""
    _ensure_database_folder()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT MAX(CAST(SUBSTR(quotation_no, 3) AS INTEGER)) FROM quotations"
        )
        result = cursor.fetchone()
        last_number = result[0] if result else None
        next_number = (last_number or 0) + 1
        return f"Q-{next_number:06d}"


def save_items(quotation_id: int, items: Iterable) -> None:
    """Save quotation items for a specific quotation."""
    _ensure_database_folder()
    with get_connection() as connection:
        cursor = connection.cursor()
        for item in items:
            cursor.execute(
                """
                INSERT INTO quotation_items(
                    quotation_id,
                    grade,
                    size,
                    quantity,
                    unit_price,
                    total
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    quotation_id,
                    item.grade,
                    item.size,
                    item.quantity,
                    item.unit_price,
                    item.total,
                ),
            )
