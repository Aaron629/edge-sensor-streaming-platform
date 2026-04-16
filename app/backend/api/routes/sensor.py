from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.backend.api.schemas.sensor import SensorDataOut, SensorStatsOut
from app.backend.database.connection import SessionLocal
from app.backend.services.sensor_service import SensorService

router = APIRouter(prefix="/sensor", tags=["sensor"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/latest", response_model=SensorDataOut)
def get_latest_sensor(
    device_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    data = SensorService.get_latest_sensor_data(
        db=db,
        device_id=device_id,
    )
    if not data:
        raise HTTPException(status_code=404, detail="No sensor data found")
    return data


@router.get("/history", response_model=List[SensorDataOut])
def get_sensor_history(
    device_id: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return SensorService.get_sensor_history(
        db=db,
        device_id=device_id,
        limit=limit,
    )


@router.get("/stats", response_model=SensorStatsOut)
def get_sensor_stats(
    device_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return SensorService.get_sensor_stats(
        db=db,
        device_id=device_id,
    )

@router.get("/latest-by-device", response_model=List[SensorDataOut])
def get_latest_sensor_by_device(
    db: Session = Depends(get_db),
):
    data = SensorService.get_latest_sensor_each_device(db=db)
    if not data:
        raise HTTPException(status_code=404, detail="No sensor data found")
    return data