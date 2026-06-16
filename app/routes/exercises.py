from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from app.forms.exercise import ExerciseForm
from app.models import Exercise

exercises_bp = Blueprint('exercises', __name__)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/new', methods=['GET', 'POST'])
def create_exercise(workout_id):
    form = ExerciseForm()
    if form.validate_on_submit():
        new_exercise = Exercise(
            name=form.name.data,
            workout_id=workout_id,
        )
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('exercises/create_exercise.html', form=form)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/update', methods=['GET', 'POST'])
def edit_exercise(workout_id, exercise_id):
    exercise = db.one_or_404(
        db.select(Exercise).where(
            Exercise.id == exercise_id,
            Exercise.workout_id == workout_id,
        )
    )

    form = ExerciseForm(obj=exercise)

    if form.validate_on_submit():
        exercise.name = form.name.data
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('exercises/create_exercise.html', form=form)


@exercises_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/delete', methods=['GET', 'POST'])
def delete_exercise(workout_id, exercise_id):
    exercise = db.one_or_404(
        db.select(Exercise).where(
            Exercise.id == exercise_id,
            Exercise.workout_id == workout_id,
        )
    )

    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('workouts.show_workout', workout_id=workout_id))
