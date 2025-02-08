from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Item, User, db
from app import app
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

item_bp = Blueprint('item_bp', __name__)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Function to check and expire items
def check_and_expire_items():
    with app.app_context():  # Ensure the app context is available
        now = datetime.utcnow()
        expired_items = Item.query.filter(Item.auction_end_time <= now, Item.status == 'active').all()
        for item in expired_items:
            item.status = 'closed'
        db.session.commit()

# Schedule the task to run every minute
scheduler.add_job(func=check_and_expire_items, trigger='interval', minutes=1)

# Create a new item for auction
@item_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Ensure only sellers or admins can create items
    if current_user.role not in ['seller', 'admin']:
        return jsonify({"error": "Unauthorized: Only sellers or admins can create items"}), 403

    # Validate required fields
    if not all(key in data for key in ['title', 'description', 'starting_price', 'auction_end_time']):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Parse auction_end_time from string to datetime
        auction_end_time = datetime.fromisoformat(data['auction_end_time'])

        # Ensure the auction end time is in the future
        if auction_end_time <= datetime.utcnow():
            return jsonify({"error": "Auction end time must be in the future"}), 400

        # Create the item
        new_item = Item(
            title=data['title'],
            description=data['description'],
            starting_price=data['starting_price'],
            current_price=data['starting_price'],  # Initialize current_price with starting_price
            auction_end_time=auction_end_time,
            seller_id=current_user_id,
            status='active'  # Set status to active by default
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({"message": "Item created successfully", "item_id": new_item.item_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all items
@item_bp.route('/items', methods=['GET'])
def get_all_items():
    items = Item.query.all()  # Fetch all items (active and closed)
    items_list = [{
        "item_id": item.item_id,
        "title": item.title,
        "description": item.description,
        "starting_price": item.starting_price,
        "current_price": item.current_price,
        "auction_end_time": item.auction_end_time.isoformat(),
        "seller_id": item.seller_id,
        "status": item.status  # Include status in the response
    } for item in items]

    return jsonify(items_list), 200

# Get a specific item by ID
@item_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    item_data = {
        "item_id": item.item_id,
        "title": item.title,
        "description": item.description,
        "starting_price": item.starting_price,
        "current_price": item.current_price,
        "auction_end_time": item.auction_end_time.isoformat(),
        "seller_id": item.seller_id,
        "status": item.status
    }

    return jsonify(item_data), 200

# Update an item
@item_bp.route('/items/<int:item_id>', methods=['PATCH'])
@jwt_required()
def update_item(item_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Ensure only the seller or admin can update the item
    if item.seller_id != current_user_id and User.query.get(current_user_id).role != 'admin':
        return jsonify({"error": "Unauthorized: Only the seller or admin can update this item"}), 403

    # Update fields if provided
    if 'title' in data:
        item.title = data['title']
    if 'description' in data:
        item.description = data['description']
    if 'starting_price' in data:
        item.starting_price = data['starting_price']
    if 'auction_end_time' in data:
        item.auction_end_time = datetime.fromisoformat(data['auction_end_time'])

    db.session.commit()
    return jsonify({"message": "Item updated successfully"}), 200

# Delete an item
@item_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    current_user_id = get_jwt_identity()
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Ensure only the seller or admin can delete the item
    if item.seller_id != current_user_id and User.query.get(current_user_id).role != 'admin':
        return jsonify({"error": "Unauthorized: Only the seller or admin can delete this item"}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200