from typing import Optional, List, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.backend.database.models.sensor_data import SensorData


class SensorRepository:

    @staticmethod
    def insert_sensor_data(db: Session, data: Dict[str, Any]) -> SensorData:
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

    @staticmethod
    def get_latest_sensor_data(
        db: Session,
        device_id: Optional[str] = None,
    ) -> Optional[SensorData]:
        stmt = select(SensorData)

        if device_id:
            stmt = stmt.where(SensorData.device_id == device_id)

        stmt = stmt.order_by(SensorData.recorded_at.desc()).limit(1)

        return db.execute(stmt).scalars().first()

    @staticmethod
    def get_sensor_history(
        db: Session,
        device_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[SensorData]:
        stmt = select(SensorData)

        if device_id:
            stmt = stmt.where(SensorData.device_id == device_id)

        stmt = stmt.order_by(SensorData.recorded_at.desc()).limit(limit)

        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_sensor_stats(
        db: Session,
        device_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        stmt = select(
            func.avg(SensorData.temperature).label("avg_temperature"),
            func.max(SensorData.temperature).label("max_temperature"),
            func.min(SensorData.temperature).label("min_temperature"),

            func.avg(SensorData.humidity).label("avg_humidity"),
            func.max(SensorData.humidity).label("max_humidity"),
            func.min(SensorData.humidity).label("min_humidity"),

            func.avg(SensorData.vibration).label("avg_vibration"),
            func.max(SensorData.vibration).label("max_vibration"),
            func.min(SensorData.vibration).label("min_vibration"),
        )

        if device_id:
            stmt = stmt.where(SensorData.device_id == device_id)

        row = db.execute(stmt).mappings().first()

        if not row:
            return {
                "avg_temperature": None,
                "max_temperature": None,
                "min_temperature": None,
                "avg_humidity": None,
                "max_humidity": None,
                "min_humidity": None,
                "avg_vibration": None,
                "max_vibration": None,
                "min_vibration": None,
            }

        return dict(row)