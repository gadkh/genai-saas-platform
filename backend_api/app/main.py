from fastapi import FastAPI
from .routers import health

app = FastAPI(title="Genai-Saas-Platform")

app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Welcome to GenAI SaaS Platform"}