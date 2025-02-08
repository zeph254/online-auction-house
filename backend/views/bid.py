from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Bid, Item, User, db
from datetime import datetime

bid_bp = Blueprint('bid_bp', __name__)

# Place a bid on an item
@bid_bp.route('/items/<int:item_id>/bids', methods=['POST'])
@jwt_required()
def place_bid(item_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Ensure the auction is still active
    if item.status != 'active':
        return jsonify({"error": "Auction is closed"}), 400

    # Ensure the auction end time hasn't passed
    if item.auction_end_time <= datetime.utcnow():
        item.status = 'closed'  # Mark the item as closed
        db.session.commit()
        return jsonify({"error": "Auction has ended"}), 400

    # Ensure the bidder is not the seller
    if item.seller_id == current_user_id:
        return jsonify({"error": "Sellers cannot bid on their own items"}), 403

    # Validate bid amount
    if 'bid_amount' not in data:
        return jsonify({"error": "Bid amount is required"}), 400

    bid_amount = data['bid_amount']
    if bid_amount <= item.current_price:
        return jsonify({"error": "Bid amount must be higher than the current price"}), 400

    try:
        # Create the bid
        new_bid = Bid(
            bid_amount=bid_amount,
            user_id=current_user_id,
            item_id=item_id
        )

        # Update the item's current price
        item.current_price = bid_amount

        db.session.add(new_bid)
        db.session.commit()

        return jsonify({"message": "Bid placed successfully", "bid_id": new_bid.bid_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all bids for an item
@bid_bp.route('/items/<int:item_id>/bids', methods=['GET'])
def get_bids_for_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    bids = Bid.query.filter_by(item_id=item_id).order_by(Bid.bid_amount.desc()).all()
    bids_list = [{
        "bid_id": bid.bid_id,
        "bid_amount": bid.bid_amount,
        "bid_time": bid.bid_time.isoformat(),
        "user_id": bid.user_id
    } for bid in bids]

    return jsonify(bids_list), 200

# Withdraw a bid
@bid_bp.route('/bids/<int:bid_id>', methods=['DELETE'])
@jwt_required()
def withdraw_bid(bid_id):
    current_user_id = get_jwt_identity()
    bid = Bid.query.get(bid_id)

    if not bid:
        return jsonify({"error": "Bid not found"}), 404

    # Ensure only the bidder can withdraw the bid
    if bid.user_id != current_user_id:
        return jsonify({"error": "Unauthorized: Only the bidder can withdraw this bid"}), 403

    db.session.delete(bid)
    db.session.commit()
    return jsonify({"message": "Bid withdrawn successfully"}), 200