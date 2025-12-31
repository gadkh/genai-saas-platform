from contextlib import asynccontextmanager
from .db.session import engine, Base
from fastapi import FastAPI

from .routers import health, api

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Genai-Saas-Platform",
              lifespan=lifespan)

app.include_router(health.router)
app.include_router(api.router)


@app.get("/")
def root():
    return {"message": "Welcome to GenAI SaaS Platform"}