import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

type SensorHistoryItem = {
  recorded_at: string;
  temperature: number | null;
  humidity: number | null;
  vibration: number | null;
};

type Props = {
  data: SensorHistoryItem[];
  dataKey: "temperature" | "humidity" | "vibration";
  title: string;
  color: string;
};

export default function MetricChart({
  data,
  dataKey,
  title,
  color,
}: Props) {
  const chartData = [...data].reverse().map((item) => ({
    ...item,
    time: new Date(item.recorded_at).toLocaleTimeString(),
  }));

  return (
    <div className="chart-card">
      <h2 className="chart-title">{title}</h2>

      <LineChart width={500} height={260} data={chartData}>
        <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" />

        <XAxis
          dataKey="time"
          tick={{ fill: "#94a3b8", fontSize: 12 }}
        />

        <YAxis
          tick={{ fill: "#94a3b8", fontSize: 12 }}
        />

        <Tooltip />

        <Line
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          strokeWidth={3}
          dot={false}
        />
      </LineChart>
    </div>
  );
}