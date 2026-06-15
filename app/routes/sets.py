from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from app.forms.sets import SetForm
from app.models.workout_set import WorkoutSet

sets_bp = Blueprint('sets', __name__)

@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/new', methods=['GET', 'POST'])
def create_set(workout_id, exercise_id):
    form = SetForm()
    if form.validate_on_submit():
        new_set = WorkoutSet(
            exercise_id = exercise_id,
            weight=form.weight.data,
            reps=form.reps.data,
        )
        db.session.add(new_set)
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('sets/create_set.html', form=form)