import time
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8081"


# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Edge Sensor Dashboard",
    page_icon="🖥️",
    layout="wide",
)


# -----------------------
# Helpers
# -----------------------
def safe_round(val, digits=2):
    return round(val, digits) if val is not None else None


def fetch_json(url: str):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return None, str(e)


def metric_card(label: str, value, unit: str = ""):
    if value is None:
        st.metric(label, "-")
    else:
        st.metric(label, f"{value}{unit}")


# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("⚙️ Control Panel")

refresh_rate = st.sidebar.slider("Refresh (seconds)", 2, 10, 5)
st.sidebar.write(f"Current refresh: {refresh_rate} sec")

auto_refresh = st.sidebar.toggle("Auto Refresh", value=True)

history_limit = st.sidebar.selectbox(
    "History limit",
    options=[30, 50, 100, 200],
    index=2,
)

st.sidebar.divider()
st.sidebar.caption("Data source: FastAPI → PostgreSQL")


# -----------------------
# Title
# -----------------------
st.title("🛰️ Edge Sensor Dashboard")
st.caption("Real-time IoT Monitoring Dashboard powered by MQTT, Kafka, FastAPI, and PostgreSQL")


# -----------------------
# Fetch Data
# -----------------------
latest, latest_err = fetch_json(f"{BASE_URL}/sensor/latest")
stats, stats_err = fetch_json(f"{BASE_URL}/sensor/stats")
history, history_err = fetch_json(f"{BASE_URL}/sensor/history?limit={history_limit}")


# -----------------------
# Error Handling
# -----------------------
if latest_err or stats_err or history_err:
    st.error("Failed to fetch data from backend API.")
    if latest_err:
        st.write(f"Latest API error: {latest_err}")
    if stats_err:
        st.write(f"Stats API error: {stats_err}")
    if history_err:
        st.write(f"History API error: {history_err}")

    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

    st.stop()


# -----------------------
# Latest Data
# -----------------------
st.markdown("## 🔴 Latest Data")

latest_col1, latest_col2, latest_col3, latest_col4 = st.columns([1, 1, 1, 1.2])

with latest_col1:
    metric_card("Temperature", safe_round(latest["temperature"]), " °C")

with latest_col2:
    metric_card("Humidity", safe_round(latest["humidity"]), " %")

with latest_col3:
    metric_card("Vibration", safe_round(latest["vibration"]))

with latest_col4:
    recorded_at = pd.to_datetime(latest["raw_payload"]["recorded_at"])
    st.metric("Recorded At", recorded_at.strftime("%Y-%m-%d %H:%M:%S"))


# -----------------------
# Alert Section
# -----------------------
alert_messages = []

if latest["temperature"] is not None and latest["temperature"] > 32:
    alert_messages.append("🔥 High temperature detected")

if latest["humidity"] is not None and latest["humidity"] > 80:
    alert_messages.append("💧 High humidity detected")

if latest["vibration"] is not None and latest["vibration"] > 0.9:
    alert_messages.append("📳 High vibration detected")

if alert_messages:
    for msg in alert_messages:
        st.error(msg)
else:
    st.success("System status normal")


st.divider()


# -----------------------
# Stats Section
# -----------------------
st.markdown("## 📊 Statistics")

temp_col, hum_col, vib_col = st.columns(3)

with temp_col:
    st.markdown("### 🌡 Temperature")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg", safe_round(stats["avg_temperature"]))
    c2.metric("Max", safe_round(stats["max_temperature"]))
    c3.metric("Min", safe_round(stats["min_temperature"]))

with hum_col:
    st.markdown("### 💧 Humidity")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg", safe_round(stats["avg_humidity"]))
    c2.metric("Max", safe_round(stats["max_humidity"]))
    c3.metric("Min", safe_round(stats["min_humidity"]))

with vib_col:
    st.markdown("### 📳 Vibration")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg", safe_round(stats["avg_vibration"]))
    c2.metric("Max", safe_round(stats["max_vibration"]))
    c3.metric("Min", safe_round(stats["min_vibration"]))


st.divider()


# -----------------------
# History Section
# -----------------------
st.markdown("## 📈 History")

df = pd.DataFrame(history)
df["recorded_at"] = pd.to_datetime(df["recorded_at"]).dt.tz_convert("Asia/Taipei")
df = df.sort_values("recorded_at")

chart_col1, chart_col2 = st.columns([3, 1])

with chart_col2:
    st.markdown("### Summary")
    st.write(f"Rows loaded: **{len(df)}**")
    st.write(f"Device ID: **{df['device_id'].iloc[0]}**" if not df.empty else "Device ID: -")
    st.write(
        f"Time range: **{df['recorded_at'].min().strftime('%H:%M:%S')} ~ {df['recorded_at'].max().strftime('%H:%M:%S')}**"
        if not df.empty
        else "Time range: -"
    )

with chart_col1:
    st.markdown("### Temperature Trend")
    st.line_chart(df.set_index("recorded_at")["temperature"], use_container_width=True)

    st.markdown("### Humidity Trend")
    st.line_chart(df.set_index("recorded_at")["humidity"], use_container_width=True)

    st.markdown("### Vibration Trend")
    st.line_chart(df.set_index("recorded_at")["vibration"], use_container_width=True)


# -----------------------
# Raw Table (Optional)
# -----------------------
with st.expander("🔍 View raw history data"):
    preview_df = df[["device_id", "temperature", "humidity", "vibration", "recorded_at"]].copy()
    preview_df["recorded_at"] = preview_df["recorded_at"].dt.strftime("%Y-%m-%d %H:%M:%S")
    st.dataframe(preview_df, use_container_width=True)


# -----------------------
# Auto Refresh
# -----------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()