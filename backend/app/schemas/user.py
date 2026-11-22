from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=100)
    phone_number: str = Field(max_length=15)
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(pattern="^(admin|student|instructor)$")


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    phone_number: str
    role: str
    created_at: datetime
    updated_at: datetime | None = None
