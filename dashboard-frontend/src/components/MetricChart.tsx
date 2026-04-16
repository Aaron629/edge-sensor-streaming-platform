import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
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

      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" />

            <XAxis
              dataKey="time"
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: "rgba(148, 163, 184, 0.2)" }}
            />

            <YAxis
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: "rgba(148, 163, 184, 0.2)" }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid rgba(148, 163, 184, 0.2)",
                borderRadius: "12px",
              }}
              labelStyle={{ color: "#94a3b8" }}
              itemStyle={{ color: "#e2e8f0" }}
            />

            <Line
              type="monotone"
              dataKey={dataKey}
              stroke={color}
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}