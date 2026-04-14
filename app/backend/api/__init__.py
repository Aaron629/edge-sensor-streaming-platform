from fastapi import APIRouter

from app.backend.api.routes.sensor import router as sensor_router

router = APIRouter()
router.include_router(sensor_router)