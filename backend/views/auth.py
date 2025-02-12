from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from models import User, db, TokenBlocklist
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
import logging

auth_bp = Blueprint('auth_bp', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified
        }
        logger.info(f"User {user.email} logged in successfully")
        return jsonify({"access_token": access_token, "user": user_data}), 200

    logger.warning(f"Failed login attempt for email: {email}")
    return jsonify({"error": "Invalid email or password"}), 401
@auth_bp.route("/current_user")
@jwt_required()
def current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_verified": user.is_verified
    }

    return jsonify(user_data), 200

@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        logger.info(f"User logged out successfully")
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during logout: {e}")
        return jsonify({"error": "An error occurred during logout"}), 500