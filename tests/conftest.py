"""Shared test fixtures.

Adds the project root to sys.path so tests can import the application
modules without installing the package.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import database  # noqa: E402


@pytest.fixture
def temp_database(tmp_path, monkeypatch):
    """Point the database module at an isolated database for one test.

    Without this, tests would read and write the developer's real
    data/steel.db and would not be repeatable.
    """
    folder = tmp_path / "data"
    monkeypatch.setattr(database, "DB_FOLDER", folder)
    monkeypatch.setattr(database, "DB_PATH", folder / "steel.db")
    database.create_database()
    return folder / "steel.db"