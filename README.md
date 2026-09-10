# Smart Room Guardian — IoT Programming Assignment 2

**SWE30011 IoT Programming — Individual Practical Project**
Arduino UNO R3 Starter Kit (IoT Node) + Raspbian on VirtualBox (Edge Device)

This repository is a self-contained guidebook + working codebase for building
**Smart Room Guardian**: a room-monitoring IoT system that reads temperature
(analog) and a door/tilt disturbance (digital) on an Arduino, streams the data
over USB serial to a Raspberry Pi (here: Raspbian running in VirtualBox),
stores it in a MariaDB database, applies a simple automation rule (edge
analytics) to drive a relay-controlled fan/appliance and a buzzer alarm, and
exposes everything through a Flask web dashboard where you can watch live
data and change the rule.

Read the docs in order — each one is short and hands-on. You do the physical
wiring and upload/run the code yourself; share photos of your wiring as you
go and this guide (and I) can sanity-check it against the wiring table.

## How the five assignment tasks map to this repo

| # | Task | Where |
|---|------|-------|
| 1 | IoT Node (sensors + actuators + sketch) | [`arduino/smart_room_guardian/`](arduino/smart_room_guardian/), [docs/04](docs/04-arduino-node.md) |
| 2 | Serial communication (both directions) | [docs/05-serial-protocol.md](docs/05-serial-protocol.md) |
| 3 | Database on Raspberry Pi (MariaDB) | [`edge/db/schema.sql`](edge/db/schema.sql), [docs/06](docs/06-database-and-analytics.md) |
| 4 | Edge analytics (conditional rule) | [`edge/iot_edge_service.py`](edge/iot_edge_service.py), [docs/06](docs/06-database-and-analytics.md) |
| 5 | User interface (dashboard) | [`edge/app.py`](edge/app.py), [`edge/templates/index.html`](edge/templates/index.html), [docs/07](docs/07-web-dashboard.md) |

## Documentation index

1. [Project summary](docs/01-project-summary.md) — background, problem, proposed system (draft for your report's Summary section)
2. [Conceptual design](docs/02-conceptual-design.md) — block diagram, sequence diagram, rule flowchart
3. [Bill of materials & wiring guide](docs/03-bill-of-materials-and-wiring.md) — **exact pin-by-pin wiring instructions**
4. [Arduino node walkthrough](docs/04-arduino-node.md) — sketch explained section by section
5. [Serial protocol](docs/05-serial-protocol.md) — the Node ⇄ Edge message format
6. [Database & edge analytics](docs/06-database-and-analytics.md) — schema, rule engine, overrides
7. [Web dashboard](docs/07-web-dashboard.md) — Flask routes, template, chart
8. [Raspbian/VirtualBox setup guide](docs/08-raspbian-vm-setup-guide.md) — **step-by-step commands**, incl. USB passthrough
9. [Testing & troubleshooting checklist](docs/09-testing-and-troubleshooting.md)
10. [Report writing guide](docs/10-report-writing-guide.md) — rubric-mapped outline + word budget
11. [Video script](docs/11-video-script.md) — 2-minute demo script, ready to record

## Repository structure

```
IoT-Programming/
├── arduino/
│   └── smart_room_guardian/
│       └── smart_room_guardian.ino   # IoT Node sketch
├── edge/
│   ├── config.py                     # serial port + DB credentials
│   ├── iot_edge_service.py           # serial reader + DB writer + rule engine
│   ├── app.py                        # Flask dashboard
│   ├── requirements.txt
│   ├── db/
│   │   └── schema.sql                # MariaDB schema + seed row
│   ├── systemd/                      # optional auto-start services
│   │   ├── iot-edge.service
│   │   └── iot-dashboard.service
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
└── docs/                             # numbered guide, see index above
```

## Quick start (after wiring is done)

```bash
sudo apt update && sudo apt install -y mariadb-server python3-venv
sudo mysql -u root -p < edge/db/schema.sql        # edit password first, see docs/08
python3 -m venv ~/iot-venv && source ~/iot-venv/bin/activate
pip install -r edge/requirements.txt
ls /dev/tty*                                       # find the Arduino's port
# edit edge/config.py with your port + DB password
python3 edge/iot_edge_service.py                   # terminal 1
python3 edge/app.py                                 # terminal 2
# open http://localhost:5000 in the VM's browser
```

Full details, including VirtualBox USB passthrough (needed for the Arduino
to be visible inside the VM at all), are in
[docs/08-raspbian-vm-setup-guide.md](docs/08-raspbian-vm-setup-guide.md).
