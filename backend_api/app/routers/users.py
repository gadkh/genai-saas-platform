from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserResponse, UserCreate
from ..services.user_service import create_user, get_user
from ..db.session import get_db
from ..deps import get_current_user
from ..db.models.user import User

router = APIRouter(prefix="/user", tags=["USER"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    exiting_user = await get_user(db=db, email=user.email)
    if exiting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = await create_user(db=db,user=user)
    return new_user

@router.get("/current", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
