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
            exercise_id=exercise_id,
            weight=form.weight.data,
            reps=form.reps.data,
        )
        db.session.add(new_set)
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('sets/create_set.html', form=form)


@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/<int:set_id>/edit', methods=['GET', 'POST'])
def edit_set(workout_id, set_id):
    set_to_update = db.get_or_404(WorkoutSet, set_id)

    form = SetForm(
        weight=set_to_update.weight,
        reps=set_to_update.reps,
    )

    if form.validate_on_submit():
        new_weight = form.weight.data
        new_reps = form.reps.data
        set_to_update.weight = new_weight
        set_to_update.reps = new_reps
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('sets/create_set.html', form=form)
