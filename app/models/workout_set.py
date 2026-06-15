from app.extensions import db
import sqlalchemy.orm as orm


class WorkoutSet(db.Model):
    __tablename__ = "workout_sets"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    exercise_id: orm.Mapped[int] = orm.mapped_column(
        db.ForeignKey("exercises.id"),
        nullable=False,
    )

    reps: orm.Mapped[int] = orm.mapped_column(
        nullable=False,
    )

    weight: orm.Mapped[float] = orm.mapped_column(
        nullable=False,
    )

    exercise = orm.relationship(
        "Exercise",
        back_populates="sets",
    )
