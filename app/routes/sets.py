from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.forms.sets import SetForm
from app.models import WorkoutSet, Exercise, Workout

sets_bp = Blueprint('sets', __name__)


@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/new', methods=['GET', 'POST'])
@login_required
def create_set(workout_id, exercise_id):
    exercise = db.one_or_404(
        db.select(Exercise)
        .join(Exercise.workout)
        .where(
            Exercise.id == exercise_id,
            Exercise.workout_id == workout_id,
            Workout.user_id == current_user.id,
        )
    )

    form = SetForm()

    if form.validate_on_submit():
        new_set = WorkoutSet(
            exercise=exercise,
            weight=form.weight.data,
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
    set_to_update = db.one_or_404(
        db.select(WorkoutSet)
        .join(WorkoutSet.exercise)
        .join(Exercise.workout)
        .where(
            WorkoutSet.id == set_id,
            Exercise.id == exercise_id,
            Exercise.workout_id == workout_id,
            Workout.user_id == current_user.id,
        )
    )

    form = SetForm(obj=set_to_update)

    if form.validate_on_submit():
        new_weight = form.weight.data
        new_reps = form.reps.data
        set_to_update.weight = new_weight
        set_to_update.reps = new_reps
        db.session.commit()
        return redirect(url_for('workouts.show_workout', workout_id=workout_id))

    return render_template('sets/create_set.html', form=form)


@sets_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/sets/<int:set_id>/delete',
               methods=['POST'])
@login_required
def delete_set(workout_id, exercise_id, set_id):
    set_to_delete = db.one_or_404(
        db.select(WorkoutSet)
        .join(WorkoutSet.exercise)
        .join(Exercise.workout)
        .where(
            WorkoutSet.id == set_id,
            Exercise.id == exercise_id,
            Exercise.workout_id == workout_id,
            Workout.user_id == current_user.id,
        )
    )
    db.session.delete(set_to_delete)
    db.session.commit()

    flash("Set deleted!", "success")

    return redirect(url_for('workouts.show_workout', workout_id=workout_id))
