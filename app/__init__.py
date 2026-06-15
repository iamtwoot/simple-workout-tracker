from flask import Flask
from app.extensions import db, migrate
from config import Config


def create_app():
    flask_app = Flask(__name__)

    flask_app.config.from_object(Config)

    db.init_app(flask_app)

    # models must be imported before migrations
    import app.models

    migrate.init_app(flask_app, db)

    # blueprints
    from app.routes.main import main_bp
    flask_app.register_blueprint(main_bp)

    from app.routes.workouts import workouts_bp
    flask_app.register_blueprint(workouts_bp)

    from app.routes.exercises import exercises_bp
    flask_app.register_blueprint(exercises_bp)

    return flask_app
