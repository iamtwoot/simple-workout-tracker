from app.extensions import db
import sqlalchemy.orm as orm

class Exercise(db.Model):
    __tablename__ = "exercises"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    workout_id: orm.Mapped[int] = orm.mapped_column(
        db.ForeignKey("workouts.id"),
        nullable=False,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        db.String(120),
        nullable=False,
    )

    order_index: orm.Mapped[int] = orm.mapped_column(
        nullable=False,
        default=0,
    )

    workout = orm.relationship(
        "Workout",
        back_populates="exercises",
    )

    sets = orm.relationship(
        "WorkoutSet",
        back_populates="exercise",
        cascade="all, delete-orphan",
        order_by="WorkoutSet.id",
    )