from flask import Blueprint,jsonify


item_bp = Blueprint('item_bp', __name__,)


@item_bp.route("/items")
def items():
    return jsonify({"items": "items"}), 200