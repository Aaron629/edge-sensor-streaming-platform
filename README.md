# 🚀 Edge Sensor Streaming Platform

## 📌 專案簡介

本專案實作一套 **IoT 即時資料串流平台（Real-time Streaming Pipeline）**，  
模擬感測器資料從裝置端（ESP32 / Python Publisher）出發，透過 MQTT 與 Kafka 進行傳輸與串流處理，  
最終落地至 PostgreSQL，並透過 FastAPI 提供服務層支援。

---

## 🧠 系統架構


```text
[ESP32 / Python Publisher]
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
```

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

### 本系統提供以下 RESTful API 供資料查詢與分析使用：

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|------------|
| GET | /sensor/latest | 取得最新一筆感測資料 |
| GET | /sensor/history | 查詢歷史資料 |
| GET | /sensor/stats | 取得統計資料（avg / max / min） |

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
│   │   ├── api/                         # FastAPI API Layer（Router / Endpoints）
│   │   │   ├── routes/
│   │   │   │   └── sensor.py
│   │   │   ├── schemas/                 # Response / Request Schema（Pydantic）
│   │   │   │   └── sensor.py
│   │   │   └── __init__.py              # 集中註冊 router
│   │   │
│   │   ├── services/                    # Business Logic Layer
│   │   │   └── sensor_service.py
│   │   │
│   │   ├── config/                      # 設定管理
│   │   │   └── settings.py
│   │   │
│   │   ├── database/                    # 資料庫層
│   │   │   ├── models/                  # ORM Model（Entity）
│   │   │   │   └── sensor_data.py
│   │   │   ├── repositories/            # Data Access Layer（CRUD / Query）
│   │   │   │   └── sensor_repository.py
│   │   │   └── connection.py            # DB 連線設定
│   │   │
│   │   ├── messaging/                   # 訊息處理（MQTT / Kafka）
│   │   │   ├── bridges/                 # MQTT → Kafka Bridge
│   │   │   │   └── mqtt_to_kafka.py
│   │   │   │
│   │   │   ├── kafka/
│   │   │   │   ├── consumers/           # Kafka Consumer（寫入 DB）
│   │   │   │   │   └── sensor_consumer.py
│   │   │   │   └── producers/           # Kafka Producer（預留）
│   │   │   │
│   │   │   └── mqtt/
│   │   │       ├── publisher/           # MQTT Publisher（模擬裝置）
│   │   │       │   └── mqtt_publisher.py
│   │   │       └── mosquitto.conf       # MQTT Broker 設定
│   │
│   └── main.py                         # FastAPI 入口（lifespan + Kafka consumer）
│
├── dashboard/                          # Dashboard（Streamlit / React）
├── docs/                               # 架構文件 / 設計說明
├── esp32/                              # ESP32 裝置端程式
│
├── docker-compose.yml                  # Kafka / MQTT / PostgreSQL
├── .env                                # 環境變數
├── requirements.txt                    # Python 套件
├── README.md
└── .gitignore
```

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

🔹 Dashboard
 即時監控（溫度 / 濕度 / 震動）
 Grafana / Streamlit / React
🔹 Data Engineering
 Databricks（Bronze / Silver / Gold）
 批次與流式分析整合
🔹 Alerting 系統
 溫度 / 震動異常偵測
 Kafka-based alert pipeline