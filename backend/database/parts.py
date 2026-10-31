from backend.models.part import Part
from backend.database.connection import get_connection

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