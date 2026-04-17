from sqlalchemy import Column, BigInteger, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from app.backend.database.connection import Base

class SnapshotType:
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT = "event"

class CameraSnapshot(Base):
    __tablename__ = "camera_snapshots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(50), nullable=False, index=True)
    sensor_data_id = Column(BigInteger, ForeignKey("sensor_data.id"), nullable=True)
    snapshot_filename = Column(String(255), nullable=False)
    snapshot_type = Column(String(30), nullable=False, default=SnapshotType.MANUAL)
    snapshot_path = Column(String(500), nullable=False)
    snapshot_url = Column(String(500), nullable=True)
    content_type = Column(String(100), nullable=False, default="image/jpeg")
    file_size = Column(Integer, nullable=True)
    source_type = Column(String(50), nullable=False, default="stream")
    status = Column(String(30), nullable=False, default="success")
    captured_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    remark = Column(String(255), nullable=True)