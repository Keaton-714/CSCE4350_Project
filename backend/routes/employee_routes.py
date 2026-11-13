from flask import Blueprint, jsonify, session, request
from backend.database.connection import get_connection
from backend.database.parts import get_store_inventory, add_part
from backend.database.purchase_orders import create_purchase_order, get_purchase_orders, receive_purchase_order, stop_purchase_order, reorder_purchase_order
from backend.database.returns import create_return, get_returns

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/api/employee/inventory", methods=["GET"])
def employee_inventory():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    if session.get("account_type") != "employee":
        return jsonify({"error": "Employee access required"}), 403

    connection = get_connection()

    try:
        employee = connection.execute(
            """
            SELECT store_id
            FROM Employee
            WHERE user_id = ?
            """,
            (session["user_id"],)
        ).fetchone()
    finally:
        connection.close()

    if employee is None:
        return jsonify({"error": "Employee not found"}), 403

    inventory = get_store_inventory(employee["store_id"])

    return jsonify(inventory)

def get_current_employee():
    if "user_id" not in session:
        return None

    if session.get("account_type") != "employee":
        return None

    connection = get_connection()

    try:
        employee = connection.execute(
            """
            SELECT employee_id, store_id
            FROM Employee
            WHERE user_id = ?
            """,
            (session["user_id"],)
        ).fetchone()

        return dict(employee) if employee else None

    finally:
        connection.close()

@employee_bp.route("/api/employee/parts", methods=["POST"])
def employee_add_part():
    employee = get_current_employee()

    if employee is None:
        return jsonify({"error": "Employee access required"}), 403

    data = request.get_json(silent=True) or {}

    name = str(data.get("name") or "").strip()
    description = str(data.get("description") or "").strip()
    category = str(data.get("category") or "").strip()

    try:
        price = float(data.get("price"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid price"}), 400

    if not name or not category or not 0 <= price < float("inf"):
        return jsonify({"error": "Invalid part information"}), 400

    part_id = add_part(name, description, price, category)

    return jsonify({"part_id": part_id}), 201

@employee_bp.route("/api/employee/orders", methods=["GET", "POST"])
def employee_orders():
    employee = get_current_employee()

    if employee is None:
        return jsonify({"error": "Employee access required"}), 403

    if request.method == "GET":
        return jsonify(get_purchase_orders(employee["store_id"]))

    data = request.get_json(silent=True) or {}
    items = data.get("items")

    if not isinstance(items, list) or not items:
        return jsonify({"error": "Order must contain parts"}), 400

    cleaned_items = []

    for item in items:
        if not isinstance(item, dict):
            return jsonify({"error": "Invalid order item"}), 400

        part_id = item.get("part_id")
        quantity = item.get("quantity")

        if (
            type(part_id) is not int
            or type(quantity) is not int
            or part_id <= 0
            or quantity <= 0
        ):
            return jsonify({"error": "Invalid part or quantity"}), 400

        cleaned_items.append({
            "part_id": part_id,
            "quantity": quantity
        })

    try:
        po_id = create_purchase_order(
            employee["employee_id"],
            employee["store_id"],
            cleaned_items
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"po_id": po_id}), 201


@employee_bp.route(
    "/api/employee/orders/<int:po_id>/receive",
    methods=["POST"]
)
def employee_receive_order(po_id):
    employee = get_current_employee()

    if employee is None:
        return jsonify({"error": "Employee access required"}), 403

    try:
        receive_purchase_order(po_id, employee["store_id"])
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"success": True})


@employee_bp.route(
    "/api/employee/orders/<int:po_id>/stop",
    methods=["POST"]
)
def employee_stop_order(po_id):
    employee = get_current_employee()

    if employee is None:
        return jsonify({"error": "Employee access required"}), 403

    try:
        stop_purchase_order(po_id, employee["store_id"])
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"success": True})


@employee_bp.route(
    "/api/employee/orders/<int:po_id>/reorder",
    methods=["POST"]
)
def employee_reorder(po_id):
    employee = get_current_employee()

    if employee is None:
        return jsonify({"error": "Employee access required"}), 403

    try:
        new_po_id = reorder_purchase_order(
            po_id,
            employee["employee_id"],
            employee["store_id"]
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"po_id": new_po_id}), 201

@employee_bp.route("/api/employee/returns", methods=["GET", "POST"])
def employee_returns():
    employee = get_current_employee()

    if employee is None:
        return jsonify({"error": "Employee access required"}), 403

    if request.method == "GET":
        returns = get_returns(employee["store_id"])
        return jsonify(returns)

    data = request.get_json(silent=True) or {}

    try:
        part_id = int(data.get("part_id"))
        quantity = int(data.get("quantity"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid part or quantity"}), 400

    reason = str(data.get("reason") or "").strip()

    if part_id <= 0 or quantity <= 0:
        return jsonify({"error": "Invalid part or quantity"}), 400

    if not reason:
        return jsonify({"error": "Return reason is required"}), 400

    try:
        return_id = create_return(
            employee["employee_id"],
            employee["store_id"],
            part_id,
            quantity,
            reason
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"return_id": return_id}), 201