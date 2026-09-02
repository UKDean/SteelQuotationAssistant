# Steel Quotation Assistant

A command-line quotation generator for reinforcing steel sales. It builds multi-item quotations, prices each line by grade and size, applies VAT, assigns sequential quotation numbers, stores everything in SQLite, and exports a formatted text quotation.

Status: early-stage, functional. Command-line interface only. No external dependencies.

---

## Problem

Preparing a rebar quotation manually means looking up the price for each grade and size, multiplying by quantity, adding VAT, numbering the document, and keeping a record of what was sent to whom. Done by hand, this is slow and error-prone, and there is no structured history of customers, projects, and quotations.

## Solution

A small Python application that captures customer, project, and line items once, computes the totals, persists the record in a local database, and produces a clean text quotation ready to send.

---

## Features

- Multiple line items per quotation (grade, size, quantity in tons)
- Automatic unit pricing by grade and size from a central price list
- Subtotal, VAT (15%), and grand total
- Sequential quotation numbering (`Q-000001`, `Q-000002`, ...) derived from the database
- Quotation date and a 7-day validity date
- SQLite persistence: customers, projects, quotations, quotation items
- Text export of each quotation to `quotations/`
- Listing of previously exported quotations

Supported grades: 60, 80
Supported sizes (mm): 10, 12, 14, 16, 18, 20, 25, 32

---

## Architecture

Each module has a single responsibility.

```
app.py                     User interface: menu, input, program flow. No SQL, no business logic.
database.py                SQLite connection, schema creation, insert and lookup functions.
models/
    item.py                Item dataclass: grade, size, quantity, unit price, line total.
    quotation.py           Quotation: items, totals, dates, numbering, text formatting.
services/
    price_service.py       Price list and price lookup.
data/                      SQLite database (created at runtime, ignored by git).
quotations/                Exported text quotations (created at runtime, ignored by git).
```

### Database schema

| Table | Purpose |
|---|---|
| `customers` | Customer name |
| `projects` | Project name, linked to a customer |
| `quotations` | Quotation number, dates, subtotal, VAT, grand total, linked to customer and project |
| `quotation_items` | Grade, size, quantity, unit price, total, linked to a quotation |

---

## Technology

- Python 3.9 or later
- Standard library only: `sqlite3`, `dataclasses`, `pathlib`, `datetime`

`requirements.txt` is intentionally empty.

---

## Installation

```powershell
git clone https://github.com/UKDean/SteelQuotationAssistant.git
cd SteelQuotationAssistant
python app.py
```

No virtual environment or package installation is required, although a virtual environment is recommended if you extend the project.

---

## Usage

```
======================================
      Steel Quotation Assistant
======================================
1. Create New Quotation
2. View Quotations
3. Exit
```

1. Choose `1`, enter the customer name and project name.
2. Enter each item: grade (60 or 80), size (mm), and quantity in tons. Invalid grade or size combinations are rejected and you are prompted again.
3. Answer `n` when finished. The quotation is printed, saved to the database, and exported to `quotations/quotation_N.txt`.
4. Choose `2` to list exported quotations.

---

## Configuration

Prices live in `services/price_service.py` as a `PRICE_LIST` dictionary keyed by grade and then size. Update this dictionary to reflect current pricing before use. VAT is fixed at 15% in `models/quotation.py`.

---

## Testing

The suite covers the price lookup, quotation totals, VAT, validity dates, text output, and SQLite persistence. Database tests run against a temporary database, so they never touch `data/steel.db`.

    python -m pip install pytest
    python -m pytest -v

30 tests, all passing.

---

## Known Issues

Quotation numbers can come from two different sources: `database.get_next_quotation_number()` reads from the database, while `Quotation.get_next_number()` counts exported text files. `app.py` uses the database, but the file-based fallback still runs when a `Quotation` is created without an explicit number, which can produce a duplicate number. Consolidating on the database as the single source of truth is pending.

## Roadmap

Planned, not yet implemented:

- Externalize the price list and VAT rate into a configuration file
- Customer and project lookup instead of creating a new record per quotation
- PDF export
- Graphical interface

---

## License

No license file is included yet. All rights reserved unless a license is added.
