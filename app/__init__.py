from flask import Flask
from app.extensions import db

# blueprints
from app.routes.main import main_bp


def create_app():
    app = Flask(__name__)

    # temporarily SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'

    db.init_app(app)

    app.register_blueprint(main_bp)

    return app