from flask import Blueprint, jsonify
from backend.database.stores import get_all_stores

store_bp = Blueprint("stores", __name__)

@store_bp.route("/api/stores", methods=["GET"])
def list_stores():
    return jsonify(get_all_stores())