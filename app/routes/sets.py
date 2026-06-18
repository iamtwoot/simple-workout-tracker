from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.forms.sets import SetForm
from app.models import WorkoutSet
from app.services.access import get_user_exercise, get_user_set

sets_bp = Blueprint('sets', __name__)


@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/new', methods=['GET', 'POST'])
@login_required
def create_set(workout_id, exercise_id):
    exercise = get_user_exercise(workout_id, exercise_id)

    form = SetForm()

    if form.validate_on_submit():
        new_set = WorkoutSet(
            exercise=exercise,
            weight=form.weight.data or 0.0,
            reps=form.reps.data,
        )
        db.session.add(new_set)
        db.session.commit()

        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('sets/create_set.html', form=form)


@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/<int:set_id>/edit',
               methods=['GET', 'POST'])
@login_required
def edit_set(workout_id, exercise_id, set_id):
    set_to_update = get_user_set(workout_id, exercise_id, set_id)

    form = SetForm(obj=set_to_update)

    if form.validate_on_submit():
        set_to_update.weight = form.weight.data or 0.0
        set_to_update.reps = form.reps.data

        db.session.commit()

        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('sets/create_set.html', form=form)


@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/<int:set_id>/delete',
               methods=['POST'])
@login_required
def delete_set(workout_id, exercise_id, set_id):
    set_to_delete = get_user_set(workout_id, exercise_id, set_id)

    db.session.delete(set_to_delete)
    db.session.commit()

    flash("Set deleted!", "success")

    return redirect(url_for('workouts.show_workout', workout_id=workout_id))
