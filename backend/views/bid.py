from flask import Blueprint,jsonify


bid_bp = Blueprint('bid_bp', __name__,)


@bid_bp.route("/bids")
def bids():
    return jsonify({"bids": "bids"}), 200