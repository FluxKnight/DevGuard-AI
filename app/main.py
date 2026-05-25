from fastapi import FastAPI
from app.api.router import api_router
from app.db.database import Base, engine
from app.models import review  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevGuard AI",
    description="AI-style code security reviewer backend",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "name": "DevGuard AI",
        "status": "running",
        "message": "Code security reviewer backend"
    }
