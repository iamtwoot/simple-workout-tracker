from flask import Flask
from app.extensions import db
from app.models.user import User


def create_app():
    import app.models

    app = Flask(__name__)

    # temporarily SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'

    db.init_app(app)

    # blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app