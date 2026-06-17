from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.delete import DeleteForm
from app.models import Workout
from app.forms.workout import WorkoutForm
from app.services.access import get_user_workout

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


@workouts_bp.route('/')
@login_required
def list_workouts():
    workouts = db.session.scalars(
        db.select(Workout)
        .where(
            Workout.user_id == current_user.id,
        )
        .order_by(Workout.workout_date.desc())
    ).all()

    delete_form = DeleteForm()

    return render_template(
        'workouts/list.html',
        workouts=workouts,
        delete_form=delete_form,
    )


@workouts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_workout():
    form = WorkoutForm()

    if form.validate_on_submit():
        new_workout = Workout(
            user_id=current_user.id,
            name=form.name.data,
        )
        db.session.add(new_workout)
        db.session.commit()

        return redirect(url_for('workouts.show_workout', workout_id=new_workout.id))

    return render_template(
        'workouts/new.html',
        form=form,
    )


@workouts_bp.route('/<int:workout_id>', methods=['GET', 'POST'])
@login_required
def show_workout(workout_id):
    workout = get_user_workout(workout_id)

    delete_form = DeleteForm()

    return render_template(
        'workouts/show_workout.html',
        workout=workout,
        delete_form=delete_form,
    )


@workouts_bp.route('/<int:workout_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_workout(workout_id):
    workout = get_user_workout(workout_id)

    form = WorkoutForm(obj=workout)

    if form.validate_on_submit():
        workout.name = form.name.data
        db.session.commit()
        return redirect(url_for('workouts.list_workouts'))

    return render_template("workouts/new.html", form=form)


@workouts_bp.route('/<int:workout_id>/delete', methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = get_user_workout(workout_id)

    db.session.delete(workout)
    db.session.commit()

    flash('Workout deleted', 'success')

    return redirect(url_for('workouts.list_workouts'))
