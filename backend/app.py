from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db, TokenBlocklist
from datetime import timedelta
import os

app = Flask(__name__)

# ✅ Allow CORS for frontend requests
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# ✅ Database & JWT setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///auction.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')  # Use environment variable
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# ✅ Import & Register Blueprints
from views import auth_bp, user_bp, item_bp, bid_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(item_bp, url_prefix='/api/item')
app.register_blueprint(bid_bp, url_prefix='/api/bid')

# ✅ Handle blocked JWTs (logout)
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist).filter_by(jti=jti).scalar()
    return token is not None

if __name__ == '__main__':
    app.run(debug=True, port=5000)