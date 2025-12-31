from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserResponse, UserCreate
from ..services.user_service import create_user, get_user
from ..db.session import get_db

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

