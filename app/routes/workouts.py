from flask import Blueprint, render_template, request
from app.extensions import db
from app.models.workout import Workout

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')

@workouts_bp.route('/', methods=['GET', 'POST'])
def home():

    workouts = db.session.execute(db.select(Workout)).scalars().all()
    return render_template('workouts/list.html', workouts=workouts)



