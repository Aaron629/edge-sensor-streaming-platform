#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ===== Wi-Fi 設定 =====
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ===== MQTT 設定 =====
const char* mqtt_server = "YOUR_MQTT_BROKER_IP";   // 你的電腦 IP
const int mqtt_port = 1883;
const char* mqtt_topic = "factory/sensor/esp32-001";
const char* mqtt_client_id = "esp32-publisher-001";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastPublishTime = 0;
const unsigned long publishInterval = 5000;

void connectWiFi() {
  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected.");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT broker... ");

    if (client.connect(mqtt_client_id)) {
      Serial.println("connected.");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retry in 3 seconds...");
      delay(3000);
    }
  }
}

String generatePayload() {
  float temperature = random(260, 330) / 10.0;
  float humidity = random(550, 800) / 10.0;
  float vibration = random(10, 100) / 100.0;

  JsonDocument doc;
  doc["device_id"] = "esp32-001";
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["vibration"] = vibration;
  doc["recorded_at"] = millis();  // 第一版先用 millis 模擬時間

  String payload;
  serializeJson(doc, payload);
  return payload;
}

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("ESP32 booting...");

  randomSeed(micros());

  connectWiFi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  unsigned long currentMillis = millis();
  if (currentMillis - lastPublishTime >= publishInterval) {
    lastPublishTime = currentMillis;

    String payload = generatePayload();

    Serial.print("Publishing to topic: ");
    Serial.println(mqtt_topic);
    Serial.print("Payload: ");
    Serial.println(payload);

    bool success = client.publish(mqtt_topic, payload.c_str());

    if (success) {
      Serial.println("Publish success.");
    } else {
      Serial.println("Publish failed.");
    }

    Serial.println("--------------------------");
  }
}