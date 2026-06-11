from datetime import datetime
from app.extensions import db
import sqlalchemy.orm as orm


class Workout(db.Model):
    __tablename__ = "workouts"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    user_id: orm.Mapped[int] = orm.mapped_column(
        db.ForeignKey("users.id"),
        nullable=False,
    )

    name: orm.Mapped[str] = orm.mapped_column(db.String(120), nullable=False)

    workout_date: orm.Mapped[datetime] = orm.mapped_column(
        db.DateTime,
        default=datetime.now,
    )

    notes: orm.Mapped[str] = orm.mapped_column(db.Text, nullable=True)

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        db.DateTime,
        default=datetime.now,
    )

    user = orm.relationship("User", back_populates="workouts")

    exercises = orm.relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
