from app.extensions import db
import sqlalchemy as sql
import sqlalchemy.orm as orm
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(sql.String(64), index=True, unique=True)
    username: orm.Mapped[str] = orm.mapped_column(sql.String(120), index=True, unique=True)
    password_hash: orm.Mapped[str] = orm.mapped_column(sql.String(256))

    created_at: orm.Mapped[datetime] = orm.mapped_column(sql.DateTime, default=datetime.now())
    updated_at: orm.Mapped[datetime] = orm.mapped_column(sql.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self) -> str:
        return f"<User {self.username}>"