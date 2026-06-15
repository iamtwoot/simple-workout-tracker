from flask import Blueprint, render_template, request
from app.extensions import db
from app.models.workout import Workout

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')

@workouts_bp.route('/')
def home():
    workouts = db.session.execute(db.select(Workout)).scalars().all()
    return render_template('workouts/list.html', workouts=workouts)

@workouts_bp.route('/new', methods=['GET', 'POST'])
def create_workout():
    return render_template('workouts/new.html')


