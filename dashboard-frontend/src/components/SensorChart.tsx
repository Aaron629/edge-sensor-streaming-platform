import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

type SensorHistoryItem = {
  id: number;
  device_id: string;
  temperature: number | null;
  humidity: number | null;
  vibration: number | null;
  recorded_at: string;
};

type Props = {
  data: SensorHistoryItem[];
};

export default function SensorChart({ data }: Props) {
  const chartData = [...data].reverse().map((item) => ({
    ...item,
    time: new Date(item.recorded_at).toLocaleTimeString(),
  }));

  return (
    <div className="chart-card">
      <h2 className="chart-title">Temperature Trend</h2>
      <LineChart width={900} height={320} data={chartData}>
        <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" />
        <XAxis dataKey="time" tick={{ fill: "#94a3b8", fontSize: 12 }} />
        <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} />
        <Tooltip />
        <Line dataKey="temperature" stroke="#60a5fa" />
        <Line dataKey="humidity" stroke="#34d399" />
        <Line dataKey="vibration" stroke="#f59e0b" />
      </LineChart>
    </div>
  );
}