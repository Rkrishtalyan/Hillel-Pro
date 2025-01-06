from flask import Flask
from app.extensions import db, migrate
from app.models import Film, Director
from app.routes import main
from app.config import Config
from flask_jwt_extended import JWTManager
from app.auth import auth_bp
from dotenv import load_dotenv
import os


load_dotenv()

def create_app():
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///film_library.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    app.register_blueprint(main)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app
