from flask import Blueprint, jsonify, request, session

from backend.database.orders import (
    create_order,
    get_customer_orders
)

order_bp = Blueprint("orders", __name__)


@order_bp.route("/api/orders", methods=["GET", "POST"])
def customer_orders():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    if session.get("account_type") != "customer":
        return jsonify({"error": "Customer access required"}), 403

    if request.method == "GET":
        return jsonify(get_customer_orders(session["user_id"]))

    data = request.get_json(silent=True) or {}

    store_id = data.get("store_id")
    items = data.get("items")

    try:
        store_id = int(store_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid store"}), 400

    if not isinstance(items, list) or not items:
        return jsonify({"error": "Cart is empty"}), 400

    cleaned_items = []
    quantities = {}

    for item in items:
        if not isinstance(item, dict):
            return jsonify({"error": "Invalid item"}), 400

        try:
            part_id = int(item["part_id"])
            quantity = int(item["quantity"])
        except (KeyError, TypeError, ValueError):
            return jsonify({"error": "Invalid part or quantity"}), 400

        if part_id <= 0 or quantity <= 0:
            return jsonify({"error": "Invalid part or quantity"}), 400

        quantities[part_id] = quantities.get(part_id, 0) + quantity

    cleaned_items = [
        {"part_id": part_id, "quantity": quantity}
        for part_id, quantity in quantities.items()
    ]

    try:
        order_id = create_order(
            session["user_id"],
            store_id,
            cleaned_items
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"order_id": order_id}), 201