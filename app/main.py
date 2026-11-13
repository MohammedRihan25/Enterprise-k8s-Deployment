import os
import socket
import time
import math
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# Pre-configured weather dataset for fast, zero-API-key reliability
WEATHER_DATA = {
    "bengaluru": {"temp_c": 26, "condition": "Partly Cloudy", "humidity": 65},
    "mumbai": {"temp_c": 31, "condition": "Humid & Sunny", "humidity": 78},
    "delhi": {"temp_c": 34, "condition": "Clear Sky", "humidity": 40},
    "gulbarga": {"temp_c": 35, "condition": "Sunny", "humidity": 38},
    "london": {"temp_c": 15, "condition": "Light Rain", "humidity": 82},
    "new york": {"temp_c": 22, "condition": "Breezy", "humidity": 55},
    "tokyo": {"temp_c": 20, "condition": "Clear", "humidity": 60},
}

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "enterprise-weather-api",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "pod_hostname": socket.gethostname(),
        "endpoints": [
            "/weather?city=<city_name>",
            "/health",
            "/stress?seconds=2"
        ]
    }), 200

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "bengaluru").lower().strip()
    data = WEATHER_DATA.get(city, {
        "temp_c": 28,
        "condition": "Moderate",
        "humidity": 50
    })
    return jsonify({
        "city": city.title(),
        "temperature_celsius": data["temp_c"],
        "condition": data["condition"],
        "humidity_percent": data["humidity"],
        "served_by_pod": socket.gethostname(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname()
    }), 200

@app.route("/stress", methods=["GET"])
def cpu_stress():
    """Simulates CPU load to trigger Kubernetes HPA auto-scaling on Day 15."""
    duration = min(float(request.args.get("seconds", 1.0)), 10.0)
    end_time = time.time() + duration
    while time.time() < end_time:
        math.sqrt(64 * 64 * 64 * 64)
    return jsonify({
        "status": "cpu_stress_completed",
        "duration_seconds": duration,
        "served_by_pod": socket.gethostname()
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
