from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SensorDataOut(BaseModel):
    id: int
    device_id: str
    temperature: float | None = None
    humidity: float | None = None
    vibration: float | None = None
    recorded_at: datetime
    created_at: datetime
    raw_payload: dict

    model_config = ConfigDict(from_attributes=True)


class SensorStatsOut(BaseModel):
    avg_temperature: float | None = None
    max_temperature: float | None = None
    min_temperature: float | None = None

    avg_humidity: float | None = None
    max_humidity: float | None = None
    min_humidity: float | None = None

    avg_vibration: float | None = None
    max_vibration: float | None = None
    min_vibration: float | None = None