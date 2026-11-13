from backend.database.connection import get_connection

from backend.database.connection import get_connection


def create_order(user_id, store_id, items):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        customer = connection.execute(
            "SELECT customer_id FROM Customer WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if customer is None:
            raise ValueError("Customer not found")

        store = connection.execute(
            "SELECT store_id FROM Store WHERE store_id = ?",
            (store_id,)
        ).fetchone()

        if store is None:
            raise ValueError("Store not found")

        # Check inventory before creating the order
        for item in items:
            stock = connection.execute(
                """
                SELECT stock_quantity
                FROM StoreInventory
                WHERE store_id = ? AND part_id = ?
                """,
                (store_id, item["part_id"])
            ).fetchone()

            if stock is None or stock["stock_quantity"] < item["quantity"]:
                raise ValueError(
                    f"Insufficient inventory for part {item['part_id']}"
                )

        cursor = connection.execute(
            """
            INSERT INTO "Order"
                (customer_id, store_id, order_date, status)
            VALUES (?, ?, CURRENT_TIMESTAMP, 'Pending')
            """,
            (customer["customer_id"], store_id)
        )

        order_id = cursor.lastrowid

        for item in items:
            part = connection.execute(
                "SELECT price FROM Part WHERE part_id = ?",
                (item["part_id"],)
            ).fetchone()

            connection.execute(
                """
                INSERT INTO OrderItem
                    (order_id, part_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
                """,
                (
                    order_id,
                    item["part_id"],
                    item["quantity"],
                    part["price"]
                )
            )

            connection.execute(
                """
                UPDATE StoreInventory
                SET stock_quantity = stock_quantity - ?
                WHERE store_id = ? AND part_id = ?
                """,
                (item["quantity"], store_id, item["part_id"])
            )

        connection.commit()
        return order_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_customer_orders(user_id):
    connection = get_connection()

    try:
        orders = connection.execute(
            """
            SELECT
                "Order".order_id,
                "Order".order_date,
                "Order".status
            FROM "Order"
            JOIN Customer
                ON "Order".customer_id = Customer.customer_id
            WHERE Customer.user_id = ?
            ORDER BY "Order".order_id DESC
            """,
            (user_id,)
        ).fetchall()

        results = []

        for order in orders:
            items = connection.execute(
                """
                SELECT
                    Part.name,
                    OrderItem.quantity,
                    OrderItem.unit_price
                FROM OrderItem
                JOIN Part ON OrderItem.part_id = Part.part_id
                WHERE OrderItem.order_id = ?
                """,
                (order["order_id"],)
            ).fetchall()

            order_items = [dict(item) for item in items]

            results.append({
                "order_id": order["order_id"],
                "order_date": order["order_date"],
                "status": order["status"],
                "items": order_items,
                "total": sum(
                    item["quantity"] * item["unit_price"]
                    for item in order_items
                )
            })

        return results

    finally:
        connection.close()