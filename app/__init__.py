from flask import Flask
from app.extensions import db, migrate


def create_app():
    flask_app = Flask(__name__)

    # temporarily SQLite
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'

    db.init_app(flask_app)

    # models must be imported before migrations
    import app.models

    migrate.init_app(flask_app, db)

    # blueprints
    from app.routes.main import main_bp
    from app.routes.workouts import workouts_bp
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(workouts_bp)

    return flask_app
