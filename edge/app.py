#!/usr/bin/env python3
"""
Web Dashboard — Smart Room Guardian
SWE30011 IoT Programming — Assignment 2

Flask application serving the assignment's user interface requirement:
  - shows the latest sensor readings and actuator states
  - visualises recent temperature history
  - shows simple analytics (mean / min / max over the last hour)
  - lets the user change the automation rule (temperature threshold)
  - lets the user manually override the fan and alarm actuators

Run with: python3 edge/app.py
Then open http://localhost:5000 in the VM's browser.
"""
from flask import Flask, jsonify, redirect, render_template, request, url_for
import mysql.connector

from config import DB_CONFIG

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def index():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 1")
    latest = cur.fetchone()

    cur.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 30")
    history = list(reversed(cur.fetchall()))

    cur.execute(
        "SELECT AVG(temperature) AS avg_t, MIN(temperature) AS min_t, "
        "MAX(temperature) AS max_t, COUNT(*) AS n FROM readings "
        "WHERE created_at >= NOW() - INTERVAL 1 HOUR"
    )
    stats = cur.fetchone()

    cur.execute("SELECT * FROM settings WHERE id = 1")
    settings = cur.fetchone()

    cur.close()
    db.close()
    return render_template(
        "index.html", latest=latest, history=history, stats=stats, settings=settings
    )


@app.route("/update_threshold", methods=["POST"])
def update_threshold():
    threshold = float(request.form["threshold"])
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE settings SET temp_threshold=%s WHERE id=1", (threshold,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for("index"))


@app.route("/override/<actuator>/<state>", methods=["POST"])
def override(actuator, state):
    if actuator not in ("fan", "alarm") or state not in ("AUTO", "ON", "OFF"):
        return "invalid request", 400
    column = "fan_override" if actuator == "fan" else "alarm_override"
    db = get_db()
    cur = db.cursor()
    cur.execute(f"UPDATE settings SET {column}=%s WHERE id=1", (state,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for("index"))


@app.route("/api/latest")
def api_latest():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 1")
    latest = cur.fetchone()
    cur.close()
    db.close()
    return jsonify(latest or {})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
