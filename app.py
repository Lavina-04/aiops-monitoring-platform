import random
import time
import json
import requests

from flask import (
    Flask,
    render_template,
    request,
    redirect
)
from prometheus_client import generate_latest, metrics
from ai_assistant.analysis_engine import generate_full_analysis
from monitoring.metrics import (
    track_request,
    get_metrics,
)
from monitoring.detector import detect_incidents
from ai_assistant.rag_engine import analyze_logs
from ai_assistant.rag_engine import generate_ai_summary

app = Flask(__name__)

attendance_counter = 0
request_number = 0

@app.route("/")
@track_request
def home():

    global request_number

    request_number += 1

   # Random latency
    time.sleep(random.uniform(0.3, 2.5))

    # Every 4th request fails
    if request_number % 4 == 0:

        return {
            "error": "Internal Server Error"
        }, 500

    return {
        "status": "running"
    }


@app.route("/incidents")
def incidents():

    detected_incidents = detect_incidents()

    try:
        with open("incident_logs.json", "r") as file:
            history = json.load(file)
    except:
        history = []

    try:
        attendance_metrics = requests.get(
            "http://127.0.0.1:5000/metrics"
        ).json()

        metrics = {
            "requests": attendance_metrics.get("requests", 0),
            "errors": attendance_metrics.get("errors", 0),
            "avg_latency": attendance_metrics.get("latency", 0),
            "uptime": 100
        }

    except Exception:
        metrics = {
            "requests": 0,
            "errors": 0,
            "avg_latency": 0,
            "uptime": 0
        }

    log_summary = analyze_logs()

    incidents = generate_full_analysis(metrics)

    return render_template(
        "dashboard.html",
        incidents=detected_incidents,
        history=history,
        metrics=metrics,
        latency_data=metrics["latency_data"],
        log_summary=log_summary
    )


@app.route("/metrics")
def metrics_endpoint():
    return generate_latest(), 200, {
        "Content-Type": "text/plain"
    }


@app.route("/api/incidents")
def api_incidents():
    return {
        "incidents": detect_incidents()
    }

@app.route("/dashboard")
def dashboard():

    metrics = get_metrics()

    incidents = generate_full_analysis(metrics)

    insights = generate_ai_summary(metrics)

    return render_template(

        "dashboard.html",

        metrics=metrics,

        incidents=incidents,

        insights=insights,

        latency_data=metrics["latency_data"]

    )

@app.route("/incidents-page")
def incidents_page():

    metrics = get_metrics()

    incidents = generate_full_analysis(metrics)
    return render_template(
        "incidents.html",
        incidents=incidents
    )


@app.route("/analysis")
def analysis():

    metrics = get_metrics()

    incidents = generate_full_analysis(metrics)
    return render_template(
        "analysis.html",
        incidents=incidents
    )


@app.route("/attendance", methods=["GET", "POST"])
@track_request
def attendance():

    global attendance_counter

    if request.method == "POST":

        attendance_counter += 1

        # 5th attendance → slow response
        if attendance_counter == 5:

            time.sleep(3)

        # 10th attendance → server error
        if attendance_counter == 10:

            return {

                "error": "Database connection failed"

            }, 500

        # Existing database insert code here

        return redirect("/dashboard")

    return render_template("attendance.html")

@app.route("/insights")
def insights():

    metrics = get_metrics()

    insights = generate_ai_summary(metrics)

    return render_template(
        "insights.html",
        insights=insights
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )