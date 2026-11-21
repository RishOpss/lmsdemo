from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime ,CheckConstraint , func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username : Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(String(255), nullable=False)
    role : Mapped[str] = mapped_column(String(20), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("length(username) >= 3", name="username_min_length"),
        CheckConstraint("length(password_hash) >= 8", name="password_min_length"),
        CheckConstraint("role IN ('admin', 'student','instructor')", name="valid_role")
    )