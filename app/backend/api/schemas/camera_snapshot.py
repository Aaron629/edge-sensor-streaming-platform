from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# 建立 snapshot（給 CRUD 用）
class CameraSnapshotCreate(BaseModel):
    device_id: str
    sensor_data_id: Optional[int] = None

    snapshot_filename: str
    snapshot_type: str = "manual"
    snapshot_path: str
    snapshot_url: Optional[str] = None

    content_type: str = "image/jpeg"
    file_size: Optional[int] = None

    source_type: str = "stream"
    status: str = "success"

    captured_at: datetime
    remark: Optional[str] = None


# API 觸發用（前端只需要給這些）
class CameraSnapshotTrigger(BaseModel):
    device_id: str
    snapshot_type: str = "manual"
    sensor_data_id: Optional[int] = None


# 回傳用（Response）
class CameraSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    sensor_data_id: Optional[int]

    snapshot_filename: str
    snapshot_type: str
    snapshot_path: str
    snapshot_url: Optional[str]

    content_type: str
    file_size: Optional[int]

    source_type: str
    status: str

    captured_at: datetime
    created_at: datetime

    remark: Optional[str]