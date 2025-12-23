from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    status: str
    service: str


class PingResponse(BaseModel):
    status: str
    db: str
    env: str

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )