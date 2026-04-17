from fastapi import APIRouter

from app.backend.api.routes.sensor import router as sensor_router
from app.backend.api.routes.camera_snapshot_router import router as camera_snapshot_router

router = APIRouter()
router.include_router(sensor_router)
router.include_router(camera_snapshot_router)