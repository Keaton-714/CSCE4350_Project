from flask import Blueprint, jsonify
from backend.database.parts import get_all_parts, get_store_inventory

part_bp = Blueprint("parts", __name__)

@part_bp.route("/api/parts", methods=["GET"])
def list_parts():
    parts = get_all_parts()

    return jsonify([part.to_dict() for part in parts])

@part_bp.route("/api/stores/<int:store_id>/inventory", methods=["GET"])
def store_inventory(store_id):
    inventory = get_store_inventory(store_id)

    return jsonify(inventory)