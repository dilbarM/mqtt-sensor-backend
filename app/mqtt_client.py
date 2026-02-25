import paho.mqtt.client as mqtt
import json
import logging
from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS, THRESHOLDS
from app.database import SessionLocal
from app.models import SensorData, Alert

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker")
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
    else:
        logger.error(f"Connection failed with code {rc}")


def on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT Broker")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
    except Exception as e:
        logger.error(f"Invalid JSON: {e}")
        return

    topic = msg.topic
    db = SessionLocal()

    try:
        sensor = SensorData(
            topic=topic,
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            voltage=data.get("voltage"),
            current=data.get("current"),
            pressure=data.get("pressure")
        )
        db.add(sensor)

        violated = []
        values = {}

        for param, limits in THRESHOLDS.items():
            value = data.get(param)

            if isinstance(value, (int, float)):
                if value < limits["min"] or value > limits["max"]:
                    violated.append(param)
                    values[param] = value

        if violated:
            alert = Alert(
                topic=topic,
                violated_keys=",".join(violated),
                actual_values=json.dumps(values)
            )
            db.add(alert)

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")

    finally:
        db.close()


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()