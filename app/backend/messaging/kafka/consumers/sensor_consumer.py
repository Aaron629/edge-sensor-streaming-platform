import json
import threading
from datetime import datetime

from kafka import KafkaConsumer

from app.backend.config.settings import settings
from app.backend.database.connection import SessionLocal
from app.backend.database.repositories.sensor_repository import SensorRepository


def parse_message(message_value: dict) -> dict:
    recorded_at_str = message_value["recorded_at"]
    recorded_at = datetime.fromisoformat(recorded_at_str)

    return {
        "device_id": message_value["device_id"],
        "temperature": message_value.get("temperature"),
        "humidity": message_value.get("humidity"),
        "vibration": message_value.get("vibration"),
        "recorded_at": recorded_at,
        "raw_payload": message_value,
    }


def consume_forever(stop_event: threading.Event) -> None:
    consumer = KafkaConsumer(
        "iot.sensor.data",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="sensor-consumer-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        consumer_timeout_ms=1000,
    )

    print("Kafka consumer started. Waiting for messages...")

    try:
        while not stop_event.is_set():
            try:
                for message in consumer:
                    if stop_event.is_set():
                        break

                    print("Received Kafka message:", message.value)

                    db = SessionLocal()
                    try:
                        parsed_data = parse_message(message.value)
                        row = SensorRepository.insert_sensor_data(db, parsed_data)
                        print(
                            f"Inserted into DB successfully. "
                            f"id={row.id}, device_id={row.device_id}, recorded_at={row.recorded_at}"
                        )
                    except Exception as e:
                        db.rollback()
                        print(f"Failed to process message: {type(e).__name__}: {e}")
                    finally:
                        db.close()
            except Exception as e:
                print(f"Kafka consume loop error: {type(e).__name__}: {e}")

    finally:
        consumer.close()
        print("Kafka consumer closed.")