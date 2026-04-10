# 🚀 Edge Sensor Streaming Platform

## 📌 專案簡介

本專案實作一套 IoT 即時資料串流平台，  
模擬感測器資料從裝置端（ESP32）出發，透過 MQTT 與 Kafka 進行傳輸與串流處理，  
最終落地至 PostgreSQL，並提供 API 與 Dashboard 進行資料查詢與視覺化分析。

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

- **Device / Publisher**
  - ESP32（Arduino / PlatformIO）
  - Python（模擬資料）

- **Messaging / Streaming**
  - MQTT（Mosquitto）
  - Kafka

- **Backend**
  - FastAPI
  - kafka-python
  - paho-mqtt

- **Database**
  - PostgreSQL

- **Visualization（規劃中）**
  - Streamlit / React

- **Environment**
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

## 📦 專案結構


edge-sensor-streaming-platform/
├─ backend/
│ ├─ app/ # FastAPI
│ ├─ consumers/ # Kafka consumer
│ ├─ bridges/ # MQTT → Kafka
│ ├─ requirements.txt
│
├─ docker-compose.yml # Kafka / MQTT / DB
├─ README.md
└─ docs/ # 架構文件（未來）


---

## 🚀 快速啟動（開發中）

### 1️⃣ 建立虛擬環境
```bash
cd backend
python -m venv venv
source venv/bin/activate
```
### 2️⃣ 安裝套件
```bash
pip install -r requirements.txt
```
### 3️⃣ 啟動服務（未完成）
```bash
docker-compose up -d
```


📡 資料格式（範例）
{
  "device_id": "esp32-001",
  "temperature": 28.5,
  "humidity": 70.2,
  "vibration": 0.23,
  "recorded_at": "2026-04-10T23:00:00+08:00"
}

🗺 未來規劃
 MQTT Publisher（ESP32 / Python）
 MQTT → Kafka Bridge
 Kafka Consumer（寫入 PostgreSQL）
 FastAPI 查詢 API
 Dashboard 視覺化（即時監控）
 Databricks 資料分析（Bronze / Silver / Gold）
 告警系統（Alerting）