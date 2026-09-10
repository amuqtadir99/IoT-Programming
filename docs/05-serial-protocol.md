# 5. Serial Protocol

A plain-text, line-based protocol over USB serial at **9600 baud, 8N1**.
Plain text was chosen deliberately: it can be read and even hand-tested
directly in the Arduino IDE's Serial Monitor, which makes debugging the
Node/Edge link far easier than a binary protocol would.

## 5.1 Node → Edge (sensor report)

Sent by the Arduino every 2 seconds (`SEND_INTERVAL_MS`):

```
T:<temperature_celsius>,D:<0|1>\n
```

| Field | Meaning | Example |
|---|---|---|
| `T` | Temperature in °C, 2 decimal places | `T:24.63` |
| `D` | Door/tilt state: `1` = triggered, `0` = at rest | `D:1` |

Full line example: `T:24.63,D:1\n`

## 5.2 Edge → Node (actuator commands)

Sent by `iot_edge_service.py` whenever an actuator's desired state changes
(not on every cycle, to avoid flooding the serial link):

| Command | Effect |
|---|---|
| `FAN:ON\n` | Energise the relay (LED "fan" load turns on) |
| `FAN:OFF\n` | De-energise the relay |
| `ALARM:ON\n` | Sound the buzzer |
| `ALARM:OFF\n` | Silence the buzzer |
| `PING\n` | Node replies `PONG\n` — useful for a manual connectivity check |

## 5.3 Design notes

- **Direction 1 satisfied:** sensor values (Node → Edge) — task 2A.
- **Direction 2 satisfied:** actuator commands (Edge → Node) — task 2B.
- The Node never blocks waiting for a command — it polls
  `Serial.available()` once per loop iteration, so sensing continues even
  if the edge device is slow or temporarily disconnected.
- The edge service only opens the serial port from **one** process at a
  time. If you have the Arduino IDE's Serial Monitor open while also
  running `iot_edge_service.py`, the Python script will fail to open the
  port (or vice versa) — close one before starting the other.
- Malformed lines (e.g. a partial line from Arduino auto-reset on connect)
  are simply skipped by the edge service rather than crashing it — see
  [docs/06](06-database-and-analytics.md).

## 5.4 Example session (as seen in a terminal)

```
$ python3 edge/iot_edge_service.py
[edge] opening serial port /dev/ttyACM0 @ 9600
[edge] T=22.10C D=0 -> FAN=OFF ALARM=OFF (threshold=30.0)
[edge] T=22.30C D=0 -> FAN=OFF ALARM=OFF (threshold=30.0)
[edge] T=31.05C D=0 -> FAN=ON ALARM=OFF (threshold=30.0)      # crossed threshold
[edge] T=31.20C D=1 -> FAN=ON ALARM=ON  (threshold=30.0)      # tilt triggered
[edge] T=30.80C D=0 -> FAN=ON ALARM=OFF (threshold=30.0)      # tilt released
```
