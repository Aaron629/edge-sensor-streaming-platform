# app/backend/database/repositories/sensor_repository.py
from sqlalchemy.orm import Session

from app.backend.database.models.sensor_data import SensorData


class SensorRepository:
    @staticmethod
    def insert_sensor_data(db: Session, data: dict) -> SensorData:
        sensor = SensorData(
            device_id=data["device_id"],
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            vibration=data.get("vibration"),
            recorded_at=data["recorded_at"],
            raw_payload=data["raw_payload"],
        )
        db.add(sensor)
        db.commit()
        db.refresh(sensor)
        return sensor