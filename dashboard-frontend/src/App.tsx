import { useEffect, useState } from "react";
import {
  getLatestSensor,
  getSensorHistory,
  getAllDevicesLatest,
} from "./api/sensorApi";
// import { ResponsiveContainer } from "recharts";
import MetricChart from "./components/MetricChart";
import "./App.css";

type SensorData = {
  id: number;
  device_id: string;
  temperature: number | null;
  humidity: number | null;
  vibration: number | null;
  recorded_at: string;
  created_at: string;
  raw_payload: Record<string, unknown>;
};

type CameraSnapshot = {
  id: number;
  device_id: string;
  sensor_data_id: number | null;
  snapshot_filename: string;
  snapshot_type: string;
  snapshot_path: string;
  snapshot_url: string | null;
  content_type: string;
  file_size: number | null;
  source_type: string;
  status: string;
  captured_at: string;
  created_at: string;
  remark: string | null;
};

function App() {
  const [data, setData] = useState<SensorData | null>(null);
  const [history, setHistory] = useState<SensorData[]>([]);
  // const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDevice, setSelectedDevice] = useState("all");
  const [allDevicesData, setAllDevicesData] = useState<SensorData[]>([]);
  const [cameraOnline, setCameraOnline] = useState(false);
  const cameraStreamUrl = "http://10.225.160.184:81/stream";
  // 快照相關狀態
  const [snapshotDevice, setSnapshotDevice] = useState("esp32-001");
  const [snapshotStart, setSnapshotStart] = useState("");
  const [snapshotEnd, setSnapshotEnd] = useState("");
  const [snapshots, setSnapshots] = useState<CameraSnapshot[]>([]);
  const [activeSnapshotIndex, setActiveSnapshotIndex] = useState(0);
  const [snapshotLoading, setSnapshotLoading] = useState(false);
  const [snapshotError, setSnapshotError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setError(null);

        if (selectedDevice === "all") {
          const allDevicesResult = await getAllDevicesLatest();

          setAllDevicesData(allDevicesResult);
          setData(null);
          setHistory([]);
          return;
        }

        const [latestResult, historyResult] = await Promise.all([
          getLatestSensor(selectedDevice),
          getSensorHistory(selectedDevice),
        ]);

        setData(latestResult);
        setHistory(historyResult);
        setAllDevicesData([]);
      } catch (err) {
        console.error(err);
        setError("讀取感測器資料失敗");
      }
    }

    fetchData();

    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, [selectedDevice]);


  if (error) return <div className="status-text">{error}</div>;

  if (selectedDevice === "all" && allDevicesData.length === 0) {
    return <div className="status-text">No data</div>;
  }

  if (selectedDevice !== "all" && !data) {
    return <div className="status-text">No data</div>;
  }

  async function handleSnapshotSearch() {
    try {
      setSnapshotLoading(true);
      setSnapshotError(null);

      const params = new URLSearchParams();
      params.append("device_id", snapshotDevice);

      if (snapshotStart) {
        params.append("start_at", new Date(snapshotStart).toISOString());
      }

      if (snapshotEnd) {
        params.append("end_at", new Date(snapshotEnd).toISOString());
      }

      params.append("limit", "20");

      const response = await fetch(
        `http://localhost:8083/camera-snapshots?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("查詢快照失敗");
      }

      const result: CameraSnapshot[] = await response.json();
      setSnapshots(result);
      setActiveSnapshotIndex(0);
    } catch (err) {
      console.error(err);
      setSnapshotError("讀取快照失敗");
      setSnapshots([]);
      setActiveSnapshotIndex(0);
    } finally {
      setSnapshotLoading(false);
    }
  }

  const activeSnapshot = snapshots[activeSnapshotIndex] ?? null;

  return (
    <div className="app">
      <div className="container">
        <header className="dashboard-header">
          <div className="header-left">
            <h1>IoT Dashboard</h1>
            <p>即時感測器監控畫面</p>
          </div>

          <div className="header-right">
            <label>Device</label>
            <select
              value={selectedDevice}
              onChange={(e) => setSelectedDevice(e.target.value)}
            >
              <option value="all">All Devices</option>
              <option value="esp32-001">esp32-001</option>
              <option value="esp32-002">esp32-002</option>
              <option value="esp32-003">esp32-003</option>
            </select>
          </div>
        </header>
        {selectedDevice === "all" ? (
          <>
            <section className="all-devices-grid">
              {allDevicesData.map((device) => (
                <div key={device.device_id} className="device-summary-card">
                  <div className="device-summary-header">
                    <h2>{device.device_id}</h2>
                    <span>{new Date(device.recorded_at).toLocaleString()}</span>
                  </div>

                  <div className="device-summary-metrics">
                    <div className="summary-metric">
                      <span className="label">Temperature</span>
                      <p className="metric-value">
                        {device.temperature !== null ? device.temperature.toFixed(2) : "--"}
                      </p>
                    </div>

                    <div className="summary-metric">
                      <span className="label">Humidity</span>
                      <p className="metric-value">
                        {device.humidity !== null ? device.humidity.toFixed(2) : "--"}
                      </p>
                    </div>

                    <div className="summary-metric">
                      <span className="label">Vibration</span>
                      <p className="metric-value">
                        {device.vibration !== null ? device.vibration.toFixed(2) : "--"}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </section>

            <section className="snapshot-explorer">
              <div className="snapshot-explorer-header">
                <div>
                  <h2>Snapshot Explorer</h2>
                  <p>依裝置與時間區段查詢歷史快照</p>
                </div>
              </div>

              <div className="snapshot-filters">
                <div className="snapshot-filter-group">
                  <label htmlFor="snapshot-device">Device</label>
                  <select
                    id="snapshot-device"
                    value={snapshotDevice}
                    onChange={(e) => setSnapshotDevice(e.target.value)}
                  >
                    <option value="esp32-001">esp32-001</option>
                    <option value="esp32-002">esp32-002</option>
                    <option value="esp32-003">esp32-003</option>
                  </select>
                </div>

                <div className="snapshot-filter-group">
                  <label htmlFor="snapshot-start">Start</label>
                  <input
                    id="snapshot-start"
                    type="datetime-local"
                    value={snapshotStart}
                    onChange={(e) => setSnapshotStart(e.target.value)}
                  />
                </div>

                <div className="snapshot-filter-group">
                  <label htmlFor="snapshot-end">End</label>
                  <input
                    id="snapshot-end"
                    type="datetime-local"
                    value={snapshotEnd}
                    onChange={(e) => setSnapshotEnd(e.target.value)}
                  />
                </div>

                <button className="snapshot-search-btn" onClick={handleSnapshotSearch}>
                  Search
                </button>
              </div>

              {snapshotLoading ? (
                <div className="snapshot-empty">Loading snapshots...</div>
              ) : snapshotError ? (
                <div className="snapshot-empty">{snapshotError}</div>
              ) : snapshots.length === 0 ? (
                <div className="snapshot-empty">尚未查詢，或此區間沒有快照</div>
              ) : activeSnapshot ? (
                <div className="snapshot-viewer">
                  <div className="snapshot-main">
                    <img
                      src={activeSnapshot.snapshot_url ?? "/camera-placeholder.jpg"}
                      alt={activeSnapshot.snapshot_filename}
                      className="snapshot-main-image"
                    />
                  </div>

                  <div className="snapshot-meta">
                    <span>Device: {activeSnapshot.device_id}</span>
                    <span>
                      Captured At: {new Date(activeSnapshot.captured_at).toLocaleString()}
                    </span>
                    <span>Type: {activeSnapshot.snapshot_type}</span>
                  </div>

                  <div className="snapshot-controls">
                    <button
                      onClick={() =>
                        setActiveSnapshotIndex((prev) => Math.max(prev - 1, 0))
                      }
                      disabled={activeSnapshotIndex === 0}
                    >
                      Prev
                    </button>

                    <span>
                      {activeSnapshotIndex + 1} / {snapshots.length}
                    </span>

                    <button
                      onClick={() =>
                        setActiveSnapshotIndex((prev) =>
                          Math.min(prev + 1, snapshots.length - 1)
                        )
                      }
                      disabled={activeSnapshotIndex === snapshots.length - 1}
                    >
                      Next
                    </button>
                  </div>
                </div>
              ) : null}
            </section>
          </>
        ) : data ? (
          <>
            <section className="overview-card">
              <div>
                <span className="label">Device ID</span>
                <p className="value">{data.device_id}</p>
              </div>
              <div>
                <span className="label">Recorded At</span>
                <p className="value">
                  {new Date(data.recorded_at).toLocaleString()}
                </p>
              </div>
            </section>

            <section className="metrics-grid">
              <div className="metric-card">
                <span className="label">Temperature</span>
                <p className="metric-value">
                  {data.temperature !== null ? data.temperature.toFixed(2) : "--"}
                </p>
              </div>

              <div className="metric-card">
                <span className="label">Humidity</span>
                <p className="metric-value">
                  {data.humidity !== null ? data.humidity.toFixed(2) : "--"}
                </p>
              </div>

              <div className="metric-card">
                <span className="label">Vibration</span>
                <p className="metric-value">
                  {data.vibration !== null ? data.vibration.toFixed(2) : "--"}
                </p>
              </div>
            </section>

            <section className="chart-grid">
              <MetricChart
                data={history}
                dataKey="temperature"
                title="Temperature Trend"
                color="#60a5fa"
              />

              <MetricChart
                data={history}
                dataKey="humidity"
                title="Humidity Trend"
                color="#34d399"
              />

              <MetricChart
                data={history}
                dataKey="vibration"
                title="Vibration Trend"
                color="#f59e0b"
              />

              <div className="camera-card">
                <div className="camera-card-header">
                  <h3>ESP32-CAM Feed</h3>
                  <span className={`camera-status ${cameraOnline ? "online" : "offline"}`}>
                    {cameraOnline ? "Online" : "Offline"}
                  </span>
                </div>

                <div className="camera-feed-wrapper">
                  <img
                    src={cameraStreamUrl}
                    alt="ESP32-CAM feed"
                    className="camera-image stream-image"
                    onLoad={() => setCameraOnline(true)}
                    onError={() => setCameraOnline(false)}
                  />

                  {!cameraOnline && (
                    <>
                      <img
                        src="/camera-placeholder.jpg"
                        alt="Camera placeholder"
                        className="camera-image placeholder-image"
                      />
                      <div className="camera-overlay">
                        <p>No camera signal</p>
                      </div>
                    </>
                  )}
                </div>

                <div className="camera-meta">
                  <span>Status: {cameraOnline ? "Online" : "Offline"}</span>
                  <span>
                    Last frame: {cameraOnline ? new Date().toLocaleTimeString() : "--"}
                  </span>
                </div>
              </div>
            </section>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default App;