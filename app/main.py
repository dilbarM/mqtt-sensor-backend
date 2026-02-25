from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
import threading
from app.database import get_db
from app.models import SensorData, Alert
from app.mqtt_client import start_mqtt

app = FastAPI(title="MQTT Sensor API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_mqtt, daemon=True).start()


@app.get("/api/sensor-data")
def get_sensor_data(page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(SensorData).order_by(desc(SensorData.timestamp))
    return {
        "total": query.count(),
        "page" : page,
        "data" : query.offset((page - 1) * limit).limit(limit).all()
    }

@app.get("/api/sensor-data/latest")
def get_latest(db: Session = Depends(get_db)):
    return db.query(SensorData).order_by(desc(SensorData.timestamp)).limit(10).all()

@app.get("/api/sensor-data/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total_messages": db.query(SensorData).count(),
        "total_alerts"  : db.query(Alert).count()
    }

@app.get("/api/alerts")
def get_alerts(page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(Alert).order_by(desc(Alert.timestamp))
    return {
        "total": query.count(),
        "page" : page,
        "data" : query.offset((page - 1) * limit).limit(limit).all()
    }

@app.get("/api/alerts/recent")
def get_recent_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(desc(Alert.timestamp)).limit(5).all()