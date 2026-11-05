from backend.database.connection import get_connection

def get_all_stores():
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT store_id, city, state
            FROM Store
            ORDER BY city
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()