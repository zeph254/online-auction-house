from flask import Flask
from models import db
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'
migrate = Migrate(app, db)

db.init_app(app)

from views import *

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(item_bp)
app.register_blueprint(bid_bp)