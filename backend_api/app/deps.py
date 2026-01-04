from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from .core.config import settings
from .db.session import get_db
from .schemas.token import TokenData
from .services.user_service import get_user

# The tokenUrl must match the path where the token endpoint is mounted
# In api.py: router = APIRouter(prefix="/v1") -> router.include_router(auth_router)
# In auth.py: @router.post("/token")
# So the full URL is /v1/token (relative to the API root, but OAuth2PasswordBearer expects a relative URL from the root of the application or absolute)
# Since app.include_router(api.router) is at root, it is /v1/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(db, email=token_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
