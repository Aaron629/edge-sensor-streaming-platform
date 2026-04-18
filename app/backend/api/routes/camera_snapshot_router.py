from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.backend.database.connection import SessionLocal
from app.backend.api.schemas.camera_snapshot import (
    CameraSnapshotRead,
    CameraSnapshotTrigger,
)
from app.backend.database.repositories.camera_snapshot_repository import CameraSnapshotRepository
from app.backend.services.camera_snapshot_service import CameraSnapshotService


router = APIRouter(
    prefix="/camera-snapshots",
    tags=["Camera Snapshots"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=CameraSnapshotRead)
def create_camera_snapshot(
    payload: CameraSnapshotTrigger,
    db: Session = Depends(get_db),
):
    snapshot_payload = CameraSnapshotService.build_stream_snapshot_payload(payload)

    snapshot = CameraSnapshotRepository.insert_camera_snapshot(
        db=db,
        payload=snapshot_payload,
    )
    return snapshot


@router.get("", response_model=List[CameraSnapshotRead])
def get_camera_snapshots(
    device_id: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return CameraSnapshotRepository.get_camera_snapshots(
        db=db,
        device_id=device_id,
        limit=limit,
    )


@router.get("/{snapshot_id}", response_model=CameraSnapshotRead)
def get_camera_snapshot_by_id(
    snapshot_id: int,
    db: Session = Depends(get_db),
):
    snapshot = CameraSnapshotRepository.get_camera_snapshot_by_id(
        db=db,
        snapshot_id=snapshot_id,
    )

    if not snapshot:
        raise HTTPException(status_code=404, detail="Camera snapshot not found")

    return snapshot