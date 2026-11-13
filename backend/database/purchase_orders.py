from backend.database.connection import get_connection


def create_purchase_order(employee_id, store_id, items, reordered_from=None):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        cursor = connection.execute(
            """
            INSERT INTO PurchaseOrder
                (employee_id, store_id, reordered_from)
            VALUES (?, ?, ?)
            """,
            (employee_id, store_id, reordered_from)
        )

        po_id = cursor.lastrowid

        for item in items:
            part_id = item["part_id"]
            quantity = item["quantity"]

            part = connection.execute(
                "SELECT price FROM Part WHERE part_id = ?",
                (part_id,)
            ).fetchone()

            if part is None:
                raise ValueError(f"Part {part_id} does not exist")

            connection.execute(
                """
                INSERT INTO PurchaseOrderItem
                    (po_id, part_id, quantity, unit_cost)
                VALUES (?, ?, ?, ?)
                """,
                (po_id, part_id, quantity, part["price"])
            )

        connection.commit()
        return po_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_purchase_orders(store_id):
    connection = get_connection()

    try:
        orders = connection.execute(
            """
            SELECT po_id, order_date, status, reordered_from
            FROM PurchaseOrder
            WHERE store_id = ?
            ORDER BY po_id DESC
            """,
            (store_id,)
        ).fetchall()

        results = []

        for order in orders:
            items = connection.execute(
                """
                SELECT
                    PurchaseOrderItem.part_id,
                    Part.name,
                    PurchaseOrderItem.quantity,
                    PurchaseOrderItem.unit_cost
                FROM PurchaseOrderItem
                JOIN Part
                    ON PurchaseOrderItem.part_id = Part.part_id
                WHERE PurchaseOrderItem.po_id = ?
                """,
                (order["po_id"],)
            ).fetchall()

            order_items = [dict(item) for item in items]

            results.append({
                "po_id": order["po_id"],
                "order_date": order["order_date"],
                "status": order["status"],
                "reordered_from": order["reordered_from"],
                "items": order_items,
                "total": sum(
                    item["quantity"] * item["unit_cost"]
                    for item in order_items
                )
            })

        return results

    finally:
        connection.close()


def receive_purchase_order(po_id, store_id):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        order = connection.execute(
            """
            SELECT status
            FROM PurchaseOrder
            WHERE po_id = ? AND store_id = ?
            """,
            (po_id, store_id)
        ).fetchone()

        if order is None:
            raise ValueError("Purchase order not found")

        if order["status"] != "Pending":
            raise ValueError("Only pending orders can be received")

        items = connection.execute(
            """
            SELECT part_id, quantity
            FROM PurchaseOrderItem
            WHERE po_id = ?
            """,
            (po_id,)
        ).fetchall()

        for item in items:
            connection.execute(
                """
                INSERT INTO StoreInventory
                    (store_id, part_id, stock_quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(store_id, part_id)
                DO UPDATE SET
                    stock_quantity = stock_quantity + excluded.stock_quantity
                """,
                (store_id, item["part_id"], item["quantity"])
            )

        connection.execute(
            """
            UPDATE PurchaseOrder
            SET status = 'Received'
            WHERE po_id = ?
            """,
            (po_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def stop_purchase_order(po_id, store_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE PurchaseOrder
            SET status = 'Stopped'
            WHERE po_id = ?
              AND store_id = ?
              AND status = 'Pending'
            """,
            (po_id, store_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Pending purchase order not found")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def reorder_purchase_order(po_id, employee_id, store_id):
    connection = get_connection()

    try:
        order = connection.execute(
            """
            SELECT po_id
            FROM PurchaseOrder
            WHERE po_id = ? AND store_id = ?
            """,
            (po_id, store_id)
        ).fetchone()

        if order is None:
            raise ValueError("Purchase order not found")

        rows = connection.execute(
            """
            SELECT part_id, quantity
            FROM PurchaseOrderItem
            WHERE po_id = ?
            """,
            (po_id,)
        ).fetchall()

        items = [dict(row) for row in rows]

    finally:
        connection.close()

    return create_purchase_order(
        employee_id,
        store_id,
        items,
        reordered_from=po_id
    )