from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='bidder')  # Default is 'bidder'
    is_verified = db.Column(db.Boolean, default=False)

    # Relationships
    items = db.relationship('Item', backref='seller', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    def __init__(self, name, email, password, role=None):
        """ Assigns the first registered user as an admin automatically. """
        existing_admin = User.query.filter_by(role='admin').first()
        self.name = name
        self.email = email
        self.password = password
        self.role = role if role else ('admin' if existing_admin is None else 'bidder')

    def __repr__(self):
        return f'<User {self.name}>'

class Item(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    auction_end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='active')  # 'active' or 'closed'

    # ForeignKey to User (seller)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Relationships
    bids = db.relationship('Bid', backref='item', lazy=True)

    def __repr__(self):
        return f'<Item {self.title}>'

class Bid(db.Model):
    __tablename__ = 'bids'

    bid_id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_time = db.Column(db.DateTime, default=datetime.utcnow)

    # ForeignKey to User (bidder)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # ForeignKey to Item
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)

    def __repr__(self):
        return f'<Bid {self.bid_amount} on Item {self.item_id} by User {self.user_id}>'
