import json
import random
import sys
import time
from datetime import datetime, timezone, timedelta

import paho.mqtt.client as mqtt


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
CLIENT_ID_PREFIX = "python-publisher"

TZ_TAIPEI = timezone(timedelta(hours=8))


def generate_sensor_payload(device_id: str) -> dict:
    base_profiles = {
        "esp32-001": {"temp_min": 26.0, "temp_max": 30.0, "hum_min": 60.0, "hum_max": 75.0, "vib_min": 0.1, "vib_max": 0.4},
        "esp32-002": {"temp_min": 28.0, "temp_max": 33.0, "hum_min": 55.0, "hum_max": 70.0, "vib_min": 0.2, "vib_max": 0.7},
        "esp32-003": {"temp_min": 27.0, "temp_max": 32.0, "hum_min": 65.0, "hum_max": 80.0, "vib_min": 0.3, "vib_max": 1.0},
    }

    profile = base_profiles.get(
        device_id,
        {"temp_min": 26.0, "temp_max": 33.0, "hum_min": 55.0, "hum_max": 80.0, "vib_min": 0.1, "vib_max": 1.0},
    )

    return {
        "device_id": device_id,
        "temperature": round(random.uniform(profile["temp_min"], profile["temp_max"]), 2),
        "humidity": round(random.uniform(profile["hum_min"], profile["hum_max"]), 2),
        "vibration": round(random.uniform(profile["vib_min"], profile["vib_max"]), 2),
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
    if len(sys.argv) < 2:
        print("Usage: python mqtt_publisher.py <device_id>")
        sys.exit(1)

    device_id = sys.argv[1]
    topic = f"factory/sensor/{device_id}"
    client_id = f"{CLIENT_ID_PREFIX}-{device_id}"

    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"Connecting to broker {MQTT_BROKER}:{MQTT_PORT} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            payload = generate_sensor_payload(device_id)
            payload_json = json.dumps(payload, ensure_ascii=False)

            print(f"Publishing to topic: {topic}")
            print(f"Payload: {payload_json}")

            result = client.publish(topic, payload_json)
            result.wait_for_publish()

            time.sleep(3)

    except KeyboardInterrupt:
        print("Stopping publisher...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()