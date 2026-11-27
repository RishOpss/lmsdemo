from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import verify_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import LoginRequest, UserRead

router = APIRouter()

@router.post("/login", response_model=UserRead)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or user.password_hash != data.password:
        raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
        )
    return user