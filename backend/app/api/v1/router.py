"""Central router aggregating all API v1 domain sub-routers."""

from fastapi import APIRouter

from app.api.v1.health import router as health_router

api_v1_router = APIRouter()

# Mount health routes
api_v1_router.include_router(health_router)
