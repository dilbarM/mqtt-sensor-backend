# MQTT Sensor

 IoT backend built with FastAPI, MQTT, and MySQL.

## Tech Stack

- FastAPI  
- MySQL  
- Eclipse Mosquitto (MQTT Broker)  
- SQLAlchemy  
- Docker & Docker Compose  

## Architecture

Simulated Sensor → MQTT Broker → FastAPI → MySQL → REST APIs → Frontend

## Features

- Subscribes to MQTT topic  
- Processes JSON sensor data  
- Stores readings in MySQL  
- Generates alerts based on thresholds  
- REST APIs with pagination  
- Fully containerized setup  

## Sensor Simulation

Sensor data is simulated by publishing JSON messages to the MQTT topic.

Example payload:

{
  "device_id": "sensor_1",
  "temperature": 32,
  "humidity": 70
}

## Run with Docker

docker compose build  
docker compose up  

Backend:  
http://localhost:8000  

API Docs:  
http://localhost:8000/docs
