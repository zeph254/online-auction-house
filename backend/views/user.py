from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import User, db


user_bp = Blueprint('user_bp', __name__,)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])

    # Check if there are any admins in the system
    existing_admin = User.query.filter_by(role="admin").first()
    
    # First user becomes admin, others become bidders
    role = "admin" if existing_admin is None else "bidder"

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User registered successfully as {role}!"}), 201



@user_bp.route('/promote/<int:user_id>', methods=['POST'])
@jwt_required()  # Ensure only logged-in users can do this
def promote_to_admin(user_id):
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    # Only admins can promote users
    if not current_user or current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.role == "admin":
        return jsonify({"message": "User is already an admin"}), 400

    user.role = "admin"
    db.session.commit()

    return jsonify({"message": f"{user.name} has been promoted to admin!"}), 200