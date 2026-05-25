from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.db.database import Base, engine
from app.models import review  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevGuard AI",
    description="AI-style code security reviewer backend",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/ui", StaticFiles(directory=str(static_path), html=True), name="ui")


@app.get("/")
def root():
    return {
        "name": "DevGuard AI",
        "status": "running",
        "message": "Code security reviewer backend",
        "ui": "/ui",
        "docs": "/docs"
    }
