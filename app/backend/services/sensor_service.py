from sqlalchemy.orm import Session

from app.backend.database.repositories.sensor_repository import SensorRepository


class SensorService:
    @staticmethod
    def get_latest_sensor_data(db: Session):
        return SensorRepository.get_latest_sensor_data(db)

    @staticmethod
    def get_sensor_history(
        db: Session,
        device_id: str | None = None,
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
        device_id: str | None = None,
    ):
        return SensorRepository.get_sensor_stats(
            db=db,
            device_id=device_id,
        )