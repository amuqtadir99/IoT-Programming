# 11. Video Demonstration Script (≤ 2 minutes)

Record with screen capture (for the dashboard/terminal parts) and your
phone/webcam (for the physical hardware parts), or do it all in one take
pointing a camera at your desk with both the breadboard and a laptop screen
visible. Practice once before recording — 2 minutes goes fast.

Timestamps are a guide, not a hard requirement — adjust pacing to fit your
actual demo, but stay under 2:00.

---

**0:00–0:15 — Intro**

> "Hi, I'm [your name], and this is my Smart Room Guardian project for
> SWE30011 IoT Programming. It's a room-monitoring system: an Arduino
> senses temperature and a door disturbance, a Raspberry Pi stores and
> analyses that data, and a web dashboard lets me watch it live and change
> the automation rule."

**0:15–0:40 — Show the hardware (IoT Node)**

*(Point the camera at the breadboard while narrating; touch each
component as you name it.)*

> "Here's the IoT node. This thermistor is my analog sensor, reading room
> temperature. This tilt switch is my digital sensor, standing in for a
> door contact. For actuators, I've got a relay here, switching this LED
> to represent a fan, and a buzzer for an alarm. All of this is driven by
> one Arduino sketch, and it talks to the Raspberry Pi over USB serial."

**0:40–1:05 — Live demo: automatic rule**

*(Warm the thermistor with your fingers.)*

> "If I warm the sensor past my threshold — currently 30 degrees — the
> edge device on the Pi picks that up and automatically turns the fan on."

*(Show/point at the relay clicking + LED lighting.)*

*(Tilt the switch.)*

> "And if I trigger the tilt sensor — simulating the door opening — the
> alarm sounds automatically too."

**1:05–1:35 — Edge device: data, database, dashboard**

*(Switch to screen capture: terminal + browser.)*

> "On the Raspberry Pi, this Python service reads the serial data, stores
> every reading in a MariaDB database, and applies the automation rule.
> Here's the web dashboard, showing the live temperature, door state, and
> actuator status, plus a chart of recent history and mean/min/max
> analytics for the last hour."

*(Change the threshold value in the dashboard form and click "Save
rule".)*

> "I can also change the rule right here — I'll lower the threshold — and
> within a couple of seconds the fan reacts to the new rule without
> touching any code."

*(Optionally click a manual override button.)*

> "I can also manually override an actuator directly from the dashboard."

**1:35–2:00 — Wrap-up**

> "That covers all five parts of the assignment: the IoT node with two
> sensors and two actuators, two-way serial communication, a MariaDB
> database storing every reading, an edge analytics rule that's changeable
> at runtime, and a web dashboard tying it all together. Thanks for
> watching."

---

## Checklist before you hit record

- [ ] Both the edge service and the dashboard are already running (start
      them a minute before recording so there's already history in the
      chart).
- [ ] Threshold is set to a value slightly above room temperature, so
      warming the thermistor visibly crosses it during the demo.
- [ ] Browser window and terminal are both visible/switchable without
      fumbling.
- [ ] Test your "warm the thermistor" action beforehand — some thermistors
      need 5–10 seconds of contact to move enough to cross a threshold, so
      know how long to hold it.
- [ ] Audio is clear if you're talking over hardware noise (relay click,
      buzzer).
