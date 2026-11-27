from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.get("/", response_model=list[UserRead])
async def read_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.post("/users", response_model=UserRead, status_code=201)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):

    new_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=user.password,
        role=user.role
    )

    session.add(new_user)

    try:
        await session.commit()

    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=409,
            detail="User data conflicts with existing records"
        )

    await session.refresh(new_user)

    return new_user