# 1. Project Summary

> Draft text for your report's "Summary" section (≈1–2 pages / 350–450 words).
> Rewrite this in your own words before submitting — use it as a scaffold,
> not a copy-paste source.

## Background

Indoor environmental monitoring is one of the most common entry points into
IoT because it combines cheap, widely available sensors with an immediately
useful outcome: knowing what is happening in a room, and reacting to it
automatically. Two well-established application patterns motivate this
project. First, **temperature-triggered automation** — appliances such as
fans, coolers, or ventilation systems that switch on automatically once a
threshold is crossed, reducing manual monitoring and energy waste. Second,
**intrusion/disturbance detection** — a low-cost tilt or vibration sensor
standing in for a door/window contact sensor, giving a simple security or
safety signal (e.g., "has this door been opened?", "has this shelf been
knocked?"). Both patterns are common in commercial smart-home products
(smart plugs with temperature rules, door/window sensors with app alerts),
which makes them a good, realistic scope for a semester-length individual
IoT project.

## Problem statement

A standalone microcontroller can sense and actuate locally, but it cannot
store history, compute trends, or present data to a user without additional
infrastructure. This project addresses that gap end-to-end: from raw analog
voltage on a breadboard, through a communication link, to a queryable
database and a browser-based dashboard a non-technical user could operate.

## Proposed system: Smart Room Guardian

**Smart Room Guardian** is a two-tier IoT system:

- **IoT Node (Arduino UNO R3):** reads room temperature via an analog NTC
  thermistor and a door/tilt disturbance via a digital tilt switch. It
  reports both values over USB serial every 2 seconds and drives two
  actuators — a relay-switched fan/appliance output and a buzzer alarm —
  based on commands received over the same serial link.
- **Edge Device (Raspberry Pi, here emulated by Raspbian in VirtualBox):**
  a Python service reads the serial stream, persists every reading into a
  MariaDB database, and applies a simple conditional rule ("if temperature
  exceeds a configurable threshold, turn the fan on; if the door/tilt sensor
  is triggered, sound the alarm"). The rule's threshold, and manual ON/OFF
  overrides for each actuator, are stored in the same database so they can
  be changed live.
- **User Interface:** a Flask web dashboard reads from the database and
  shows the current temperature, door state, and actuator states; a line
  chart of recent temperature history; mean/min/max analytics over the last
  hour; a form to edit the automation threshold; and buttons to manually
  override each actuator — closing the loop between user, edge analytics,
  and physical hardware.

## Objectives

1. Build a working IoT Node with one analog sensor, one digital sensor, and
   two actuators, controlled by a single Arduino sketch.
2. Establish bidirectional serial communication between the Node and the
   Edge device.
3. Persist sensor data into a MariaDB database running on the edge device.
4. Implement an edge-side conditional rule that reacts to sensor data by
   commanding the Node's actuators, with the rule changeable at runtime.
5. Provide a web dashboard for live monitoring, historical visualisation,
   and rule/actuator control.

## Scope and limitations

The relay output switches a low-voltage LED (simulating a fan/appliance)
rather than a mains-powered appliance, for safety and because a breadboard
kit is not mains-rated. The system is a proof-of-concept intended to
demonstrate the IoT architecture (sense → communicate → store → analyse →
act → visualise) rather than a production-grade deployment.
