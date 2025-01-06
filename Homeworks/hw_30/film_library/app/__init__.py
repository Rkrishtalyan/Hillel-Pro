from flask import Flask
from app.extensions import db, migrate
from app.models import Film, Director
from app.routes import main
from app.config import Config


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///film_library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
