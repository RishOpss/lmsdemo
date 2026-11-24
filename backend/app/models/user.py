from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    username: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "length(username) >= 3",
            name="username_min_length"
        ),
        CheckConstraint(
            "length(password_hash) >= 8",
            name="password_min_length"
        ),
        CheckConstraint(
            "role IN ('admin', 'student', 'instructor')",
            name="valid_role"
        )
    )