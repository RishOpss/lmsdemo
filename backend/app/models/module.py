from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime ,CheckConstraint , func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Module(Base):
    __tablename__ = "modules"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id : Mapped[int] = mapped_column(Integer, nullable=False)
    title : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description : Mapped[str] = mapped_column(String(255), nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("length(title) >= 5", name="title_min_length"),
    )