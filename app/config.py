import os
from dotenv import load_dotenv 
load_dotenv()

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL is not set in the env variables")
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

MQTT_TOPICS = [
    "sensors/device1", 
    "sensors/device2",
    "sensors/device3",
    "sensors/device4",
    "sensors/device5",
    "sensors/device6",
    "sensors/device7",            
]


THRESHOLDS = {
    "temperature": {"min": 0, "max": 80},
    "humidity": {"min": 20, "max": 90},
    "voltage" :{"min":210, "max":250},
    "current" :{"min":0, "max":15},
    "pressure" :{"min":950, "max":1050},
}