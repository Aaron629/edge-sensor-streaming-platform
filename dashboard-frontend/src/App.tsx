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

function App() {
  const [data, setData] = useState<SensorData | null>(null);
  const [history, setHistory] = useState<SensorData[]>([]);
  // const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDevice, setSelectedDevice] = useState("all");
  const [allDevicesData, setAllDevicesData] = useState<SensorData[]>([]);
  const [cameraOnline, setCameraOnline] = useState(false);

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

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>IoT Dashboard</h1>
          <p className="subtitle">即時感測器監控畫面</p>
          <div className="device-filter">
            <label htmlFor="device-select" className="device-filter-label">
              Device
            </label>
            <select
              id="device-select"
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
                  {!cameraOnline && (
                    <div className="camera-overlay">
                      <p>No camera signal</p>
                    </div>
                  )}

                  <img
                    src="http://10.225.160.184:81/stream"
                    className="camera-image"
                    onLoad={() => setCameraOnline(true)}
                    onError={() => setCameraOnline(false)}
                  />
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