def generate_full_analysis(metrics):

    incidents = []

    requests = metrics["requests"]
    errors = metrics["errors"]
    latency = metrics["avg_latency"]
    uptime = metrics["uptime"]

    # -------------------------
    # HIGH LATENCY
    # -------------------------

    if latency > 200:

        incidents.append({

            "type": "High Latency",

            "severity": "High",

            "priority": "P2",

            "cause":
            f"Average response time reached {latency} ms, indicating backend or database bottlenecks.",

            "solution": [
                "Optimize database queries",
                "Scale backend services",
                "Enable caching mechanisms"
            ]

        })

    # -------------------------
    # HIGH ERROR RATE
    # -------------------------

    error_rate = 0

    if requests > 0:

        error_rate = (errors / requests) * 100

    if error_rate > 3:

        incidents.append({

            "type": "High Error Rate",

            "severity": "Critical",

            "priority": "P1",

            "cause":
            f"Application error rate is {error_rate:.1f}%, indicating unstable services or failed dependencies.",

            "solution": [
                "Inspect server logs",
                "Restart unhealthy services",
                "Verify backend dependencies"
            ]

        })

    # -------------------------
    # LOW UPTIME
    # -------------------------

    if uptime < 90:

        incidents.append({

            "type": "Service Degradation",

            "severity": "Medium",

            "priority": "P3",

            "cause":
            f"System uptime dropped to {uptime}% which is below operational expectations.",

            "solution": [
                "Investigate service interruptions",
                "Review application health checks",
                "Monitor infrastructure stability"
            ]

        })

    # -------------------------
    # TRAFFIC SURGE
    # -------------------------

    if requests > 20:

        incidents.append({

            "type": "Traffic Surge",

            "severity": "Medium",

            "priority": "P3",

            "cause":
            f"System handled {requests} requests in a short period, indicating increased load.",

            "solution": [
                "Scale application instances",
                "Enable load balancing",
                "Monitor resource utilization"
            ]

        })

    return incidents