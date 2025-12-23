from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.health import HealthCheck, PingResponse
from ..services.health_service import is_db_online

router = APIRouter(prefix="/health", tags=["HEALTH"])


@router.get("/alive", response_model=HealthCheck)
def check_liveness():
    return HealthCheck(status="ok", service="genai_saas_platform_backend")


@router.get("/ping", response_model=PingResponse)
def get_readiness():
    is_online = is_db_online()
    if not is_online:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="DB connection is failed"
        )
    return PingResponse(status="pong", db="connected", env="dev")