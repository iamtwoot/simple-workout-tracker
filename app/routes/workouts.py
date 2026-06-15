from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models.workout import Workout
from app.forms.workout import WorkoutForm

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


@workouts_bp.route('/')
def list_workouts():
    workouts = db.session.execute(db.select(Workout)).scalars().all()
    return render_template(
        'workouts/list.html',
        workouts=workouts,
    )


@workouts_bp.route('/new', methods=['GET', 'POST'])
def create_workout():
    form = WorkoutForm()

    if form.validate_on_submit():
        new_workout = Workout(
            # replace with current_user.id
            user_id=1,
            name=form.name.data,
        )
        db.session.add(new_workout)
        db.session.commit()

        return redirect(url_for('workouts.list_workouts'))

    return render_template(
        'workouts/new.html',
        form=form,
    )


@workouts_bp.route('/<int:workout_id>')
def show_workout(workout_id):
    workout = db.get_or_404(Workout, workout_id)
    return render_template(
        'workouts/show_workout.html',
        workout=workout,
    )
