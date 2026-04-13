# 🚀 Edge Sensor Streaming Platform

## 📌 專案簡介

本專案實作一套 **IoT 即時資料串流平台（Real-time Streaming Pipeline）**，  
模擬感測器資料從裝置端（ESP32 / Python Publisher）出發，透過 MQTT 與 Kafka 進行傳輸與串流處理，  
最終落地至 PostgreSQL，並透過 FastAPI 提供服務層支援。

---

## 🧠 系統架構


ESP32 / Python Publisher
↓
MQTT Broker
↓
MQTT → Kafka Bridge
↓
Kafka
↓
Kafka Consumer
↓
PostgreSQL
↓
FastAPI
↓
Dashboard


---

## 🛠 技術棧

### 🔌 Device / Publisher
- ESP32（Arduino / PlatformIO）
- Python（模擬感測資料）

### 📡 Messaging / Streaming
- MQTT（Mosquitto）
- Kafka（KRaft mode）
- kafka-python
- paho-mqtt

### ⚙️ Backend
- FastAPI
- SQLAlchemy

### 🗄 Database
- PostgreSQL

### 🧪 Environment
- Docker Compose
- Python venv

---

## 🎯 專案目標

- 建立 IoT 裝置到資料庫的完整資料流（End-to-End Pipeline）
- 熟悉 MQTT 與 Kafka 的串流整合
- 實作資料接收、處理與儲存流程
- 建立即時監控與資料分析能力
- 作為 AIoT / Data Engineering / Backend 系統設計作品

---

## 📂 專案結構

```text
edge-sensor-streaming-platform/
├── app/
│   ├── backend/
│   │   ├── api/                     # FastAPI API（未來擴充）
│   │   ├── config/                  # 設定管理
│   │   │   └── settings.py
│   │   │
│   │   ├── database/                # 資料庫相關
│   │   │   ├── models/              # ORM Model
│   │   │   │   └── sensor_data.py
│   │   │   ├── repositories/        # 資料存取層（CRUD）
│   │   │   │   └── sensor_repository.py
│   │   │   └── connection.py        # DB 連線設定
│   │   │
│   │   ├── messaging/               # 訊息處理（MQTT / Kafka）
│   │   │   ├── bridges/             # MQTT → Kafka
│   │   │   │   └── mqtt_to_kafka.py
│   │   │   │
│   │   │   ├── kafka/
│   │   │   │   ├── consumers/       # Kafka Consumer（落地 DB）
│   │   │   │   │   └── sensor_consumer.py
│   │   │   │   └── producers/       # Kafka Producer（預留）
│   │   │   │
│   │   │   └── mqtt/
│   │   │       ├── publisher/       # MQTT Publisher（模擬裝置）
│   │   │       │   └── mqtt_publisher.py
│   │   │       └── mosquitto.conf   # MQTT Broker 設定
│   │
│   └── main.py                     # FastAPI entrypoint（含 lifespan + consumer）
│
├── dashboard/                      # 儀表板（未來實作）
├── doc/                            # 文件（架構 / 設計）
├── esp32/                          # ESP32 程式（實體裝置）
│
├── mqtt/                           # MQTT 相關設定（若有額外配置）
│
├── docker-compose.yml              # Kafka / MQTT / PostgreSQL
├── .env                            # 環境變數
├── requirements.txt                # Python 套件
├── README.md
└── .gitignore


---

## 🚀 快速啟動（開發中）

### 1️⃣ 啟動基礎服務（MQTT / Kafka / DB）
```bash
docker compose up -d
```
### 2️⃣ 建立 Python 環境
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### 3️⃣ 啟動 FastAPI（含 Kafka Consumer）
```bash
uvicorn app.main:app --reload --port 8081
```
### 4️⃣ 啟動 Publisher（模擬資料）
```bash
python -m app.backend.messaging.mqtt.publisher.mqtt_publisher
```

🎯 專案亮點
🔥 Event-Driven Architecture

使用 Kafka 作為資料中介，實現鬆耦合資料流

🔥 Streaming Pipeline

資料從裝置即時流入資料庫（非批次處理）

🔥 Schema + Raw Data 設計

同時支援：

查詢效率（結構化欄位）
完整回溯（raw_payload）
🔥 IoT + Data Engineering 整合

整合：

MQTT（IoT）
Kafka（Streaming）
PostgreSQL（Storage）


📡 資料格式（範例）
{
  "device_id": "esp32-001",
  "temperature": 28.5,
  "humidity": 70.2,
  "vibration": 0.23,
  "recorded_at": "2026-04-10T23:00:00+08:00"
}

🗺 未來規劃
🔹 API 層
 /sensor/latest
 /sensor/history
 /sensor/stats
🔹 Dashboard
 即時監控（溫度 / 濕度 / 震動）
 Grafana / Streamlit / React
🔹 Data Engineering
 Databricks（Bronze / Silver / Gold）
 批次與流式分析整合
🔹 Alerting 系統
 溫度 / 震動異常偵測
 Kafka-based alert pipeline