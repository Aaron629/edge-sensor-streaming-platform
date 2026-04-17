from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple
import shutil

from app.backend.api.schemas.camera_snapshot import (
    CameraSnapshotCreate,
    CameraSnapshotTrigger,
)


class SnapshotSourceType:
    MOCK = "mock"
    STREAM = "stream"


class CameraSnapshotService:
    SNAPSHOT_ROOT = Path("storage/snapshots")
    MOCK_IMAGE_PATH = Path("app/static/mock/camera-placeholder.png")

    @staticmethod
    def ensure_snapshot_dir(device_id: str, captured_at: datetime) -> Path:
        folder = (
            CameraSnapshotService.SNAPSHOT_ROOT
            / device_id
            / captured_at.strftime("%Y-%m-%d")
        )
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @staticmethod
    def generate_snapshot_filename(device_id: str, captured_at: datetime) -> str:
        return f"{device_id}_{captured_at.strftime('%Y%m%d_%H%M%S')}.jpg"

    @staticmethod
    def save_mock_snapshot_file(device_id: str, captured_at: datetime) -> Tuple[str, str, int]:
        if not CameraSnapshotService.MOCK_IMAGE_PATH.exists():
            raise FileNotFoundError(
                f"Mock image not found: {CameraSnapshotService.MOCK_IMAGE_PATH}"
            )

        folder = CameraSnapshotService.ensure_snapshot_dir(
            device_id=device_id,
            captured_at=captured_at,
        )
        filename = CameraSnapshotService.generate_snapshot_filename(
            device_id=device_id,
            captured_at=captured_at,
        )
        filepath = folder / filename

        shutil.copy(CameraSnapshotService.MOCK_IMAGE_PATH, filepath)

        file_size = filepath.stat().st_size
        return filename, str(filepath), file_size

    @staticmethod
    def build_mock_snapshot_payload(trigger: CameraSnapshotTrigger) -> CameraSnapshotCreate:
        captured_at = datetime.now(timezone.utc)

        filename, filepath, file_size = CameraSnapshotService.save_mock_snapshot_file(
            device_id=trigger.device_id,
            captured_at=captured_at,
        )
        # 前端存取快照路徑（實際部署時可能需要調整 URL 結構）
        snapshot_url = f"/storage/snapshots/{trigger.device_id}/{captured_at.strftime('%Y-%m-%d')}/{filename}"

        return CameraSnapshotCreate(
            device_id=trigger.device_id,
            sensor_data_id=trigger.sensor_data_id,
            snapshot_filename=filename,
            snapshot_type=trigger.snapshot_type,
            snapshot_path=filepath,
            snapshot_url=snapshot_url,
            content_type="image/jpeg",
            file_size=file_size,
            source_type=SnapshotSourceType.MOCK,
            status="success",
            captured_at=captured_at,
            remark="Mock snapshot generated for testing",
        )