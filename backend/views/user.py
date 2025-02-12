from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import User, db
from flask_cors import cross_origin  # ✅ Import this


user_bp = Blueprint('user_bp', __name__)

# ✅ Handle preflight OPTIONS request properly
@user_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def register():
    if request.method == 'OPTIONS':  # ✅ Handle preflight requests
        return jsonify({"message": "Preflight request successful"}), 200

    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    existing_admin = User.query.filter_by(role="admin").first()
    role = "admin" if existing_admin is None else "bidder"

    new_user = User(name=data["name"], email=data["email"], password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User registered successfully as {role}!"}), 201





@user_bp.route('/promote/<int:user_id>', methods=['POST'])
@jwt_required()  # Ensure only logged-in users can do this
def promote_to_admin(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)


    # Only admins can promote users
    if not current_user or current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.role == "admin":
        return jsonify({"message": "User is already an admin"}), 400

    # Prevent the last admin from demoting themselves
    total_admins = User.query.filter_by(role="admin").count()
    if total_admins == 1 and user.user_id == current_user.user_id:
        return jsonify({"error": "Cannot demote the last admin"}), 403

    user.role = "admin"
    db.session.commit()

    return jsonify({"message": f"{user.name} has been promoted to admin!"}), 200


@user_bp.route('/update/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if user:    
        data = request.get_json()

        # Use .get() method correctly
        name = data.get('name', user.name)
        email = data.get('email', user.email)
        password = data.get('password', user.password)

        # Hash the password only if a new password is provided
        if password != user.password:
            password = generate_password_hash(password)

        # Check if the new name or email already exists (excluding the current user)
        check_name = User.query.filter(User.name == name, User.user_id != user_id).first()
        check_email = User.query.filter(User.email == email, User.user_id != user_id).first()

        if check_name or check_email:
            return jsonify({"error": "Username or email already exists"}), 400
        
        else:
            user.name = name
            user.email = email
            user.password = password

            db.session.commit()
            return jsonify({"message": f"User has been updated"}), 200

    else:
        return jsonify({"message": "User doesn't exist"}), 404

@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if user:    
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User has been deleted"}), 200
    
    else:
        return jsonify({"message": "User doesn't exist"}), 404