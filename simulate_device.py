import paho.mqtt.client as mqtt
import json
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883)

print("Connected to MQTT Broker...")

NUM_DEVICES = 5

try:
    while True:
        for i in range(1, NUM_DEVICES + 1):
            topic = f"sensors/device{i}"

            data = {
                "temperature": round(random.uniform(20, 100), 2),
                "humidity": round(random.uniform(30, 90), 2),
                "voltage": round(random.uniform(210, 250), 2),
                "current": round(random.uniform(1, 15), 2),
                "pressure": round(random.uniform(950, 1050), 2),
            }

            client.publish(topic, json.dumps(data))
            print(f"Sent to {topic}: {data}")

        print("Batch Sent\n")
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopped by user.")

client.disconnect()