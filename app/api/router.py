from fastapi import APIRouter
from app.api.routes import health, reviews, reports

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
