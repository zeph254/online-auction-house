from flask import Blueprint,jsonify


auth_bp = Blueprint('auth_bp', __name__,)


@auth_bp.route("/auth")
def auth():
    return jsonify({"auth": "auth"}), 200