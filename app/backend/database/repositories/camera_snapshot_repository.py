from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database.models.camera_snapshot import CameraSnapshot
from app.backend.api.schemas.camera_snapshot import CameraSnapshotCreate


class CameraSnapshotRepository:

    @staticmethod
    def insert_camera_snapshot(
        db: Session,
        payload: CameraSnapshotCreate,
    ) -> CameraSnapshot:
        snapshot = CameraSnapshot(
            device_id=payload.device_id,
            sensor_data_id=payload.sensor_data_id,
            snapshot_filename=payload.snapshot_filename,
            snapshot_type=payload.snapshot_type,
            snapshot_path=payload.snapshot_path,
            snapshot_url=payload.snapshot_url,
            content_type=payload.content_type,
            file_size=payload.file_size,
            source_type=payload.source_type,
            status=payload.status,
            captured_at=payload.captured_at,
            remark=payload.remark,
        )
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return snapshot

    @staticmethod
    def get_camera_snapshot_by_id(
        db: Session,
        snapshot_id: int,
    ) -> Optional[CameraSnapshot]:
        stmt = select(CameraSnapshot).where(CameraSnapshot.id == snapshot_id)
        return db.execute(stmt).scalars().first()

    @staticmethod
    def get_camera_snapshots(
        db: Session,
        device_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[CameraSnapshot]:
        stmt = select(CameraSnapshot)

        if device_id:
            stmt = stmt.where(CameraSnapshot.device_id == device_id)

        stmt = stmt.order_by(CameraSnapshot.captured_at.desc()).limit(limit)

        return list(db.execute(stmt).scalars().all())