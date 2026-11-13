from backend.database.connection import get_connection


def create_return(employee_id, store_id, part_id, quantity, reason):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        # Ensure the part exists
        part = connection.execute(
            "SELECT part_id FROM Part WHERE part_id = ?",
            (part_id,)
        ).fetchone()

        if part is None:
            raise ValueError("Part not found")

        # Record the return
        cursor = connection.execute(
            """
            INSERT INTO ReturnRecord
                (employee_id, store_id, part_id, quantity, reason)
            VALUES (?, ?, ?, ?, ?)
            """,
            (employee_id, store_id, part_id, quantity, reason)
        )

        return_id = cursor.lastrowid

        # Increase inventory
        connection.execute(
            """
            INSERT INTO StoreInventory
                (store_id, part_id, stock_quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(store_id, part_id)
            DO UPDATE SET
                stock_quantity = stock_quantity + excluded.stock_quantity
            """,
            (store_id, part_id, quantity)
        )

        connection.commit()
        return return_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_returns(store_id):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                ReturnRecord.return_id,
                ReturnRecord.part_id,
                Part.name,
                ReturnRecord.quantity,
                ReturnRecord.reason,
                ReturnRecord.return_date
            FROM ReturnRecord
            JOIN Part
                ON ReturnRecord.part_id = Part.part_id
            WHERE ReturnRecord.store_id = ?
            ORDER BY ReturnRecord.return_id DESC
            """,
            (store_id,)
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()