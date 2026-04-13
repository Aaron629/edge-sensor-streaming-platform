from sqlalchemy import Column, BigInteger, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.backend.database.connection import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(50), nullable=False, index=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    vibration = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False, index=True)
    raw_payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)