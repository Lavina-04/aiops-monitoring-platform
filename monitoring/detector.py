from ai_assistant.rag_engine import (
    analyze_incident,
    calculate_anomaly_score
)

import monitoring.metrics as metrics

from logs.logger import log_incident


# ----------------------------
# SAFE RAG WRAPPER
# ----------------------------
def safe_analyze_incident(issue_type):

    try:

        analysis = analyze_incident(issue_type)

        if not isinstance(analysis, dict):
            raise ValueError("Invalid analysis format")

        return {
            "cause": analysis.get(
                "cause",
                "Unknown cause"
            ),

            "solution": analysis.get(
                "solution",
                "No solution available"
            ),

            "knowledge": analysis.get(
                "knowledge",
                ["No knowledge available"]
            )
        }

    except Exception:

        return {
            "cause": "Analysis failed",

            "solution":
            "Check RAG engine or model response format",

            "knowledge":
            ["No operational knowledge available"]
        }


# ----------------------------
# INCIDENT DETECTION ENGINE
# ----------------------------
def detect_incidents():
    print("\n========== DETECTOR ==========")
    print("REQUESTS:", metrics.request_count)
    print("ERRORS:", metrics.error_count)
    print("LATENCIES:", len(metrics.response_times))

    incidents = []

    # ----------------------------
    # HIGH LATENCY DETECTION
    # ----------------------------
    if metrics.response_times and len(metrics.response_times) > 0:

        avg_latency = (
            sum(metrics.response_times)
            / len(metrics.response_times)
        )
         
        print("AVG LATENCY:", avg_latency)

        if avg_latency > 1000:

            analysis = safe_analyze_incident(
                "High Latency"
            )

            anomaly = calculate_anomaly_score(
                avg_latency
            )

            incident = {

                "type": "High Latency",

                "severity": "High",

                "value": f"{avg_latency:.2f} ms",

                "cause": analysis["cause"],

                "solution": analysis["solution"],

                "knowledge": analysis["knowledge"],

                "score": anomaly["score"],

                "risk": anomaly["risk"],

                "priority": anomaly["priority"],

                "actions": anomaly["action"]

            }

            incidents.append(incident)

            log_incident(incident)

    # ----------------------------
    # HIGH ERROR RATE DETECTION
    # ----------------------------
    if metrics.request_count > 0:

        error_rate = (
            metrics.error_count / metrics.request_count
        ) * 100
        print("REQUEST COUNT:", metrics.request_count)
        print("ERROR COUNT:", metrics.error_count)

        if error_rate > 20:

            analysis = safe_analyze_incident(
                "High Error Rate"
            )

            anomaly = calculate_anomaly_score(
                error_rate
            )

            incident = {

                "type": "High Error Rate",

                "severity": "Critical",

                "value": f"{error_rate:.2f}%",

                "cause": analysis["cause"],

                "solution": analysis["solution"],

                "knowledge": analysis["knowledge"],

                "score": anomaly["score"],

                "risk": anomaly["risk"],

                "priority": anomaly["priority"],

                "actions": anomaly["action"]

            }

            incidents.append(incident)

            log_incident(incident)

    return incidents