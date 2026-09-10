#!/usr/bin/env python3
"""
IoT Edge Service — Smart Room Guardian
SWE30011 IoT Programming — Assignment 2

Runs continuously on the Raspberry Pi / Raspbian VM. Responsibilities:

  1. Serial communication with the Arduino IoT Node (docs/05-serial-protocol.md).
  2. Persist every sensor reading into the MariaDB database (docs/06).
  3. Apply the edge analytics rule (temperature threshold, door/tilt alarm).
  4. Send actuator commands back to the Arduino node when a decision changes.

Run with: python3 edge/iot_edge_service.py
Stop with Ctrl+C.
"""
import time

import mysql.connector
import serial

from config import SERIAL_PORT, BAUD_RATE, DB_CONFIG


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def get_settings(db):
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM settings WHERE id = 1")
    row = cur.fetchone()
    cur.close()
    return row


def insert_reading(db, temperature, door, fan_state, alarm_state):
    cur = db.cursor()
    cur.execute(
        "INSERT INTO readings (temperature, door_tilt, fan_state, alarm_state) "
        "VALUES (%s, %s, %s, %s)",
        (temperature, door, int(fan_state), int(alarm_state)),
    )
    db.commit()
    cur.close()


def decide_state(auto_condition, override):
    """AUTO defers to the rule; ON/OFF force the actuator regardless of sensors."""
    if override == "ON":
        return True
    if override == "OFF":
        return False
    return auto_condition


def main():
    print(f"[edge] opening serial port {SERIAL_PORT} @ {BAUD_RATE}")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    time.sleep(2)  # let the Arduino finish its power-on-open auto-reset

    db = get_db()
    last_fan_state = None
    last_alarm_state = None
    line = ""

    while True:
        try:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw.startswith("T:"):
                continue
            line = raw

            parts = dict(field.split(":") for field in line.split(","))
            temperature = float(parts["T"])
            door = int(parts["D"])

            settings = get_settings(db)
            threshold = float(settings["temp_threshold"])

            fan_on = decide_state(temperature > threshold, settings["fan_override"])
            alarm_on = decide_state(door == 1, settings["alarm_override"])

            if fan_on != last_fan_state:
                ser.write(b"FAN:ON\n" if fan_on else b"FAN:OFF\n")
                last_fan_state = fan_on
            if alarm_on != last_alarm_state:
                ser.write(b"ALARM:ON\n" if alarm_on else b"ALARM:OFF\n")
                last_alarm_state = alarm_on

            insert_reading(db, temperature, door, fan_on, alarm_on)

            print(
                f"[edge] T={temperature:.2f}C D={door} -> "
                f"FAN={'ON' if fan_on else 'OFF'} "
                f"ALARM={'ON' if alarm_on else 'OFF'} (threshold={threshold})"
            )

        except (ValueError, KeyError) as exc:
            print(f"[edge] skipping malformed line: {line!r} ({exc})")
        except mysql.connector.Error as exc:
            print(f"[edge] DB error: {exc}, reconnecting in 2s...")
            time.sleep(2)
            db = get_db()
        except KeyboardInterrupt:
            print("\n[edge] stopping.")
            break

    ser.close()
    db.close()


if __name__ == "__main__":
    main()
