from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, ConfigDict


class SensorDataOut(BaseModel):
    id: int
    device_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    vibration: Optional[float] = None
    recorded_at: datetime
    created_at: datetime
    raw_payload: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class SensorStatsOut(BaseModel):
    avg_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    min_temperature: Optional[float] = None

    avg_humidity: Optional[float] = None
    max_humidity: Optional[float] = None
    min_humidity: Optional[float] = None

    avg_vibration: Optional[float] = None
    max_vibration: Optional[float] = None
    min_vibration: Optional[float] = None