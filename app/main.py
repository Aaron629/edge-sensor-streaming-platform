import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.backend.api import router as api_router
from app.backend.config.settings import settings
from app.backend.database.connection import Base, engine
from app.backend.database.models.sensor_data import SensorData
from app.backend.messaging.kafka.consumers.sensor_consumer import consume_forever


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting application...")

    # 建表
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created (if not exist)")
    except Exception as e:
        logger.exception(f"❌ Failed to initialize database: {e}")
        raise

    stop_event = None
    consumer_thread = None

    if settings.ENABLE_KAFKA_CONSUMER:
        try:
            stop_event = threading.Event()
            consumer_thread = threading.Thread(
                target=consume_forever,
                args=(stop_event,),
                daemon=True,
                name="kafka-consumer-thread",
            )
            consumer_thread.start()
            logger.info("✅ Kafka consumer thread started")
        except Exception as e:
            logger.warning(f"⚠️ Kafka consumer start failed: {e}")
            logger.warning("⚠️ Application will continue running without Kafka consumer")

    app.state.kafka_stop_event = stop_event
    app.state.kafka_consumer_thread = consumer_thread

    yield

    logger.info("🛑 Shutting down application...")

    try:
        if app.state.kafka_stop_event:
            app.state.kafka_stop_event.set()

        if app.state.kafka_consumer_thread:
            app.state.kafka_consumer_thread.join(timeout=5)

        logger.info("✅ Kafka consumer thread stopped")
    except Exception as e:
        logger.error(f"❌ Error stopping Kafka consumer: {e}")


app = FastAPI(
    title="Edge Sensor Streaming Platform",
    lifespan=lifespan,
)


app.include_router(api_router)

