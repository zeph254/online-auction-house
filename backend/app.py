from flask import Flask
from models import TokenBlocklist, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'
migrate = Migrate(app, db)

db.init_app(app)


jwt = JWTManager(app)
jwt.init_app(app)

app.config['JWT_SECRET_KEY'] = 'https6789069954321t2wndpd'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 24)


from views import *
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(item_bp)
app.register_blueprint(bid_bp)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload)->bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist).filter_by(jti=jti).scalar()
    return token is not None