const API_BASE = "http://localhost:8083";

export async function getLatestSensor(deviceId: string) {
  const url =
    deviceId === "all"
      ? `${API_BASE}/sensor/latest`
      : `${API_BASE}/sensor/latest?device_id=${encodeURIComponent(deviceId)}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch latest sensor: ${response.status}`);
  }

  return response.json();
}

export async function getSensorHistory(deviceId: string) {
  const url =
    deviceId === "all"
      ? `${API_BASE}/sensor/history`
      : `${API_BASE}/sensor/history?device_id=${encodeURIComponent(deviceId)}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch sensor history: ${response.status}`);
  }

  return response.json();
}

export async function getAllDevicesLatest() {
  const response = await fetch(`${API_BASE}/sensor/latest-by-device`);

  if (!response.ok) {
    throw new Error(`Failed to fetch all devices latest data: ${response.status}`);
  }

  return response.json();
}