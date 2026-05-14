from fastapi import APIRouter

from app.api.routers import health, adoption, survey, report

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(adoption.router, prefix="/adoption", tags=["adoption"])
api_router.include_router(survey.router, prefix="/survey")
api_router.include_router(report.router, prefix="/report", tags=["report"])
