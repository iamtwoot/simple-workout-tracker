from flask_login import current_user
from app import db
from app.models import Workout, Exercise, WorkoutSet


def get_user_workout(workout_id):
    return db.one_or_404(
        db.select(Workout).where(
            Workout.user_id == current_user.id,
            Workout.id == workout_id,
        )
    )


def get_user_exercise(workout_id, exercise_id):
    return db.one_or_404(
        db.select(Exercise)
        .join(Exercise.workout)
        .where(
            Exercise.id == exercise_id,
            Workout.id == workout_id,
            Workout.user_id == current_user.id,
        )
    )


def get_user_set(workout_id, exercise_id, set_id):
    return db.one_or_404(
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
