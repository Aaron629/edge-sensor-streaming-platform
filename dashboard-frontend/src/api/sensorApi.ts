const BASE_URL = "http://localhost:8083";

export async function getLatestSensor(deviceId?: string) {
  const url = deviceId
    ? `${BASE_URL}/sensor/latest?device_id=${deviceId}`
    : `${BASE_URL}/sensor/latest`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch latest sensor data");
  }

  return response.json();
}

export async function getSensorHistory(deviceId?: string) {
  const url = deviceId
    ? `${BASE_URL}/sensor/history?device_id=${deviceId}&limit=20`
    : `${BASE_URL}/sensor/history?limit=20`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch sensor history");
  }

  return response.json();
}