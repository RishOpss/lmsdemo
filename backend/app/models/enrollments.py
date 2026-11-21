from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime ,CheckConstraint , func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(Integer, nullable=False)
    course_id : Mapped[int] = mapped_column(Integer, nullable=False)
    enrolled_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())