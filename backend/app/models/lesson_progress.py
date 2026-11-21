from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime ,CheckConstraint , func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(Integer, nullable=False)
    lesson_id : Mapped[int] = mapped_column(Integer, nullable=False)
    progress : Mapped[int] = mapped_column(Integer, nullable=False)  # Progress percentage (0-100)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("progress >= 0 AND progress <= 100", name="valid_progress"),
    )