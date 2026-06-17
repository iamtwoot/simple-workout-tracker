from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.exercise import ExerciseForm
from app.models import Exercise, Workout

exercises_bp = Blueprint('exercises', __name__)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/new', methods=['GET', 'POST'])
@login_required
def create_exercise(workout_id):
    # Check if this workout belongs to the current user
    workout = db.one_or_404(
        db.select(Workout).where(
            Workout.id == workout_id,
            Workout.user_id == current_user.id,
        )
    )

    form = ExerciseForm()

    if form.validate_on_submit():
        new_exercise = Exercise(
            name=form.name.data,
            workout=workout,
        )
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('exercises/create_exercise.html', form=form)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/update', methods=['GET', 'POST'])
@login_required
def edit_exercise(workout_id, exercise_id):
    # Check if the exercise belongs to the current user
    exercise = db.one_or_404(
        db.select(Exercise)
        .join(Exercise.workout)
        .where(
            Exercise.id == exercise_id,
            Workout.id == workout_id,
            Workout.user_id == current_user.id,
        )
    )

    form = ExerciseForm(obj=exercise)

    if form.validate_on_submit():
        exercise.name = form.name.data
        db.session.commit()

        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('exercises/create_exercise.html', form=form)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/delete', methods=['POST'])
def delete_exercise(workout_id, exercise_id):
    # Check if the exercise belongs to the current user
    exercise = db.one_or_404(
        db.select(Exercise)
        .join(Exercise.workout)
        .where(
            Exercise.id == exercise_id,
            Workout.id == workout_id,
            Workout.user_id == current_user.id,
        )
    )

    db.session.delete(exercise)
    db.session.commit()

    flash("Exercise deleted!", "success")

    return redirect(url_for('workouts.show_workout', workout_id=workout_id))
