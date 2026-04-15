import { useEffect, useState } from "react";
import { getLatestSensor, getSensorHistory } from "./api/sensorApi";

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

  useEffect(() => {
    async function fetchData() {
      try {
        const [latestResult, historyResult] = await Promise.all([
          getLatestSensor(),
          getSensorHistory(),
        ]);
        setData(latestResult);
        setHistory(historyResult);
      } catch (err) {
        setError("讀取感測器資料失敗");
      }
    }

    fetchData();

    const interval = setInterval(fetchData, 3000); // 每 3 秒更新

    return () => clearInterval(interval);
  }, []);


  if (error) return <div className="status-text">{error}</div>;
  if (!data) return <div className="status-text">No data</div>;

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>IoT Dashboard</h1>
          <p className="subtitle">即時感測器監控畫面</p>
        </header>

        <section className="overview-card">
          <div>
            <span className="label">Device ID</span>
            <p className="value">{data.device_id}</p>
          </div>
          <div>
            <span className="label">Recorded At</span>
            <p className="value">{new Date(data.recorded_at).toLocaleString()}</p>
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
        </section>
      </div>
    </div>
  );
}

export default App;