# Project Handover for Codex

## Project

Steel Quotation Assistant

The goal is to build a professional desktop quotation system for Al Rajhi Steel using Python.

This is NOT a learning project.

The final goal is a production-quality application.

---

## Current Project Structure

app.py

database.py

models/
    item.py
    quotation.py

services/
    price_service.py

data/

quotations/

---

## Current Features

Working quotation model.

Multiple quotation items.

Automatic pricing.

VAT calculation.

Grand total.

Quotation numbering.

TXT quotation export.

SQLite database.

---

## Database Tables

customers

projects

quotations

quotation_items

---

## Current Issue

The project originally worked correctly.

Many code snippets were copied manually from ChatGPT.

This introduced:

incorrect indentation

duplicate functions

wrong imports

calling functions before importing them

mixed responsibilities between app.py and database.py

The goal is NOT to rewrite everything.

The goal is to repair the architecture while preserving all existing functionality.

---

## Responsibilities

app.py

Only user interface.

Menus.

Inputs.

Program flow.

No SQL.

No database logic.

No business logic.

database.py

SQLite connection.

Table creation.

CRUD functions.

Only database operations.

models/item.py

Item model only.

models/quotation.py

Quotation model only.

Calculations.

Formatting.

services/price_service.py

Pricing logic only.

---

## Coding Rules

Never remove working functionality.

Prefer refactoring over rewriting.

Preserve project structure.

Follow PEP8.

Avoid duplicate code.

Avoid global variables.

Keep each file responsible for a single purpose.

---

## Roadmap

Phase 1

Repair architecture.

Fix imports.

Fix indentation.

Fix runtime errors.

Repair database integration.

Phase 2

Customer management.

Project management.

Quotation history.

Quotation editing.

Quotation deletion.

Phase 3

Professional PDF quotation.

Company logo.

Company information.

Payment terms.

Delivery terms.

Signature.

QR Code.

Phase 4

Dashboard.

Search.

Reports.

Statistics.

Excel export.

Backup.

Restore.

Settings.

Phase 5

Professional desktop application.

Windows installer.

Executable EXE.

---

## Current Request

Do NOT rewrite the project.

First inspect every file.

Explain all problems.

Then repair the project incrementally.

After every change explain what was modified.

Never delete working code unless absolutely necessary.

Always keep the application runnable.
