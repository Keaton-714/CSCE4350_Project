from backend.models.part import Part
from backend.database.connection import get_connection

def get_all_parts():
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT part_id, name, description, price, category
            FROM Part
            ORDER BY name
            """
        )

        rows = cursor.fetchall()

        parts = []

        for row in rows:
            part = Part(
                part_id=row["part_id"],
                name=row["name"],
                description=row["description"],
                price=row["price"],
                category=row["category"]
            )

            parts.append(part)

        return parts

    finally:
        connection.close()

def get_store_inventory(store_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                Part.part_id,
                Part.name,
                Part.description,
                Part.price,
                Part.category,
                StoreInventory.stock_quantity
            FROM Part
            JOIN StoreInventory
                ON Part.part_id = StoreInventory.part_id
            WHERE StoreInventory.store_id = ?
            ORDER BY Part.name
            """,
            (store_id,)
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()

def get_part(part_id):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT part_id, name, description, price, category
            FROM Part
            WHERE part_id = ?
            """,
            (part_id,)
        ).fetchone()

        if row is None:
            return None

        part = Part(
            row["part_id"],
            row["name"],
            row["description"],
            row["price"],
            row["category"]
        )

        return part
    finally:
        connection.close()

def add_part(name, description, price, category):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO Part (name, description, price, category)
            VALUES (?, ?, ?, ?)
            """,
            (name, description, price, category)
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()