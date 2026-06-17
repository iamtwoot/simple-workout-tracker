from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import func
from app.extensions import db
from app.forms.exercise import ExerciseForm
from app.models import Exercise
from app.services.access import get_user_workout, get_user_exercise

exercises_bp = Blueprint('exercises', __name__)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/new', methods=['GET', 'POST'])
@login_required
def create_exercise(workout_id):
    workout = get_user_workout(workout_id)

    form = ExerciseForm()

    if form.validate_on_submit():
        max_order = db.session.scalar(
            db.select(func.max(Exercise.order_index))
            .where(Exercise.workout_id == workout_id)
        )

        new_exercise = Exercise(
            name=form.name.data,
            workout=workout,
            order_index=(max_order or 0) + 1,
        )

        db.session.add(new_exercise)
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('exercises/create_exercise.html', form=form)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/update', methods=['GET', 'POST'])
@login_required
def edit_exercise(workout_id, exercise_id):
    exercise = get_user_exercise(workout_id, exercise_id)

    form = ExerciseForm(obj=exercise)

    if form.validate_on_submit():
        exercise.name = form.name.data
        db.session.commit()

        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('exercises/create_exercise.html', form=form)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/delete', methods=['POST'])
def delete_exercise(workout_id, exercise_id):
    exercise = get_user_exercise(workout_id, exercise_id)

    db.session.delete(exercise)
    db.session.commit()

    flash("Exercise deleted!", "success")

    return redirect(url_for('workouts.show_workout', workout_id=workout_id))
