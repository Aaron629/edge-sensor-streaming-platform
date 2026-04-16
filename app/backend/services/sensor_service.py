from typing import Optional

from sqlalchemy.orm import Session

from app.backend.database.repositories.sensor_repository import SensorRepository


class SensorService:
    @staticmethod
    def get_latest_sensor_data(
        db: Session,
        device_id: Optional[str] = None,
    ):
        return SensorRepository.get_latest_sensor_data(
            db=db,
            device_id=device_id,
        )
    
    @staticmethod
    def get_latest_sensor_each_device(
        db: Session,
    ):
        return SensorRepository.get_latest_sensor_each_device(db=db)

    @staticmethod
    def get_sensor_history(
        db: Session,
        device_id: Optional[str] = None,
        limit: int = 100,
    ):
        return SensorRepository.get_sensor_history(
            db=db,
            device_id=device_id,
            limit=limit,
        )

    @staticmethod
    def get_sensor_stats(
        db: Session,
        device_id: Optional[str] = None,
    ):
        return SensorRepository.get_sensor_stats(
            db=db,
            device_id=device_id,
        )