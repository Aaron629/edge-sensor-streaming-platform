import json
import random
import time
from datetime import datetime, timezone, timedelta

import paho.mqtt.client as mqtt


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/sensor/esp32-001"
CLIENT_ID = "python-publisher-001"

TZ_TAIPEI = timezone(timedelta(hours=8))


def generate_sensor_payload() -> dict:
    return {
        "device_id": "esp32-001",
        "temperature": round(random.uniform(26.0, 33.0), 2),
        "humidity": round(random.uniform(55.0, 80.0), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2),
        "recorded_at": datetime.now(TZ_TAIPEI).isoformat(),
    }


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully.")
    else:
        print(f"Failed to connect to MQTT broker. rc={rc}")


def on_publish(client, userdata, mid):
    print(f"Message published successfully. mid={mid}")


def main():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"Connecting to broker {MQTT_BROKER}:{MQTT_PORT} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            payload = generate_sensor_payload()
            payload_json = json.dumps(payload, ensure_ascii=False)

            print(f"Publishing to topic: {MQTT_TOPIC}")
            print(f"Payload: {payload_json}")

            result = client.publish(MQTT_TOPIC, payload_json)
            result.wait_for_publish()

            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping publisher...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()