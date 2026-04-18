from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple
import requests

from app.backend.api.schemas.camera_snapshot import (
    CameraSnapshotCreate,
    CameraSnapshotTrigger,
)


class SnapshotSourceType:
    MOCK = "mock"
    STREAM = "stream"


class CameraSnapshotService:
    SNAPSHOT_ROOT = Path("storage/snapshots")
    BASE_URL = "http://localhost:8083"

    # 依你目前前端 stream URL 推測，capture 多半是這個
    CAMERA_CAPTURE_URL = "http://10.225.160.184/capture"

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
    def fetch_camera_snapshot() -> bytes:
        """
        從 ESP32-CAM 抓取單張圖片
        """
        response = requests.get(
            CameraSnapshotService.CAMERA_CAPTURE_URL,
            timeout=10,
        )
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "image" not in content_type.lower():
            raise ValueError(
                f"Camera capture did not return an image. content-type={content_type}"
            )

        return response.content

    @staticmethod
    def save_stream_snapshot_file(
        device_id: str,
        captured_at: datetime,
    ) -> Tuple[str, str, int]:
        image_bytes = CameraSnapshotService.fetch_camera_snapshot()

        folder = CameraSnapshotService.ensure_snapshot_dir(
            device_id=device_id,
            captured_at=captured_at,
        )
        filename = CameraSnapshotService.generate_snapshot_filename(
            device_id=device_id,
            captured_at=captured_at,
        )
        filepath = folder / filename

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        file_size = filepath.stat().st_size
        return filename, str(filepath), file_size

    @staticmethod
    def build_stream_snapshot_payload(
        trigger: CameraSnapshotTrigger,
    ) -> CameraSnapshotCreate:
        captured_at = datetime.now(timezone.utc)

        filename, filepath, file_size = CameraSnapshotService.save_stream_snapshot_file(
            device_id=trigger.device_id,
            captured_at=captured_at,
        )

        relative_url = (
            f"/storage/snapshots/"
            f"{trigger.device_id}/{captured_at.strftime('%Y-%m-%d')}/{filename}"
        )
        snapshot_url = f"{CameraSnapshotService.BASE_URL}{relative_url}"

        return CameraSnapshotCreate(
            device_id=trigger.device_id,
            sensor_data_id=trigger.sensor_data_id,
            snapshot_filename=filename,
            snapshot_type=trigger.snapshot_type,
            snapshot_path=filepath,
            snapshot_url=snapshot_url,
            content_type="image/jpeg",
            file_size=file_size,
            source_type=SnapshotSourceType.STREAM,
            status="success",
            captured_at=captured_at,
            remark="Snapshot captured from ESP32-CAM",
        )