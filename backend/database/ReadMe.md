# Auto Parts System — Database Setup Guide

## Overview

This folder contains the SQLite database for our CSCE 4350 Auto Parts System project.

**Files:**
- `schema.sql` — Creates all eight database tables, including primary keys, foreign keys, and constraints.
- `test_data.sql` — Adds fictional sample data for development and testing.
- `auto_parts.db` — Local SQLite database file. This is excluded from GitHub using `.gitignore`.

## 1. Create the Database

Open a terminal in the project's root directory and run:

```bash
sqlite3 backend/database/auto_parts.db < backend/database/schema.sql
```

This creates the database file and its eight tables.

## 2. Load Sample Data (Optional)

To populate the database with test records, run:

```bash
sqlite3 backend/database/auto_parts.db < backend/database/test_data.sql
```

The sample data includes parts, a store, users, customers, an employee, inventory, and an order.

## 3. Verify the Database

Run:

```bash
sqlite3 backend/database/auto_parts.db ".tables"
```

The database should contain:

- Part
- Store
- User
- Employee
- Customer
- StoreInventory
- Order
- OrderItem

## 4. Enable Foreign Keys in Flask

SQLite requires foreign-key enforcement to be enabled for each database connection.

Example:

```python
import sqlite3

conn = sqlite3.connect("backend/database/auto_parts.db")
conn