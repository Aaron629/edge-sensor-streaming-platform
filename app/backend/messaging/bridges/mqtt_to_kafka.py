import json
from kafka import KafkaProducer
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/sensor/esp32-001"

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "iot.sensor.data"


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# 初始化 Kafka Producer
def init_kafka_producer():
    try:
        # 增加 api_version 可以大幅減少連線錯誤
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version=(3, 9, 2), # 對應你的 docker image 版本
            retries=5
        )
        print("Kafka Producer initialized successfully.")
        return producer
    except Exception as e:
        print(f"Failed to initialize Kafka Producer: {e}")
        return None

producer = init_kafka_producer()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker.")
        
        # 🔥 關鍵：訂閱所有裝置
        topic = "factory/sensor/#"
        client.subscribe(topic)
        
        print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect to MQTT broker. rc={rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")

    print(f"\n📡 Topic: {msg.topic}")
    print(f"📦 Payload: {payload}")

    try:
        data = json.loads(payload)

        producer.send(KAFKA_TOPIC, value=data)
        producer.flush()

        print(f"➡️ Sent to Kafka topic: {KAFKA_TOPIC}")

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Kafka send error: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to MQTT broker {MQTT_BROKER}:{MQTT_PORT} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()