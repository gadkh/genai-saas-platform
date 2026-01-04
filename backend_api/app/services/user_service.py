from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_hashed_password


async def get_user(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_hashed_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        credits=10,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user
