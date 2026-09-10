# 2. Conceptual Design

Use these three diagrams (rendered directly by GitHub) as the "Conceptual
design" figures in your report. Screenshot them or re-draw them in
draw.io/Lucidchart if your report format needs static images.

## 2.1 System block diagram (hardware/software architecture)

```mermaid
flowchart LR
    subgraph NODE["IoT Node — Arduino UNO R3"]
        TH["Thermistor (analog sensor, A0)"]
        TS["Tilt switch (digital sensor, D2)"]
        UNO["ATmega328P + sketch"]
        RLY["Relay module (D8)"]
        BUZ["Buzzer (D9)"]
        LOAD["LED load = simulated fan/appliance"]
        TH --> UNO
        TS --> UNO
        UNO --> RLY --> LOAD
        UNO --> BUZ
    end

    subgraph EDGE["Edge Device — Raspbian (VirtualBox VM)"]
        SVC["iot_edge_service.py<br/>(serial I/O + rule engine)"]
        DB[("MariaDB<br/>iot_project")]
        WEB["Flask app.py"]
        DASH["Web dashboard (browser)"]
        SVC --> DB
        DB --> WEB
        WEB --> DASH
    end

    UNO <-->|"USB serial, 9600 baud"| SVC
    DASH -->|"update threshold / override actuator"| DB
    SVC -->|"read settings each cycle"| DB
```

**Narrative:** the Node is a pure sense-and-act device — it has no logic
beyond reading pins and obeying ON/OFF commands. All decision-making
("edge analytics") happens in `iot_edge_service.py` on the Pi, which is the
architecture the assignment asks for (IoT Node ⇄ Edge Device). The database
is the shared state between the analytics service and the dashboard: the
service writes readings and reads settings; the dashboard reads readings and
writes settings. Neither talks to the other directly, which avoids two
processes fighting over the same serial port.

## 2.2 Sequence diagram — one control loop

```mermaid
sequenceDiagram
    participant A as Arduino (Node)
    participant P as iot_edge_service.py
    participant D as MariaDB
    participant F as Flask dashboard
    participant U as User (browser)

    loop every 2 seconds
        A->>P: "T:24.50,D:0"
        P->>D: SELECT settings (threshold, overrides)
        D-->>P: threshold=30.0, fan_override=AUTO, alarm_override=AUTO
        P->>P: evaluate rule (temp > threshold? door == 1?)
        alt actuator state changed
            P->>A: "FAN:ON" / "FAN:OFF" / "ALARM:ON" / "ALARM:OFF"
        end
        P->>D: INSERT INTO readings (temp, door, fan_state, alarm_state)
    end

    U->>F: edit threshold / click override button
    F->>D: UPDATE settings
    U->>F: GET /  (page auto-refreshes every 10s)
    F->>D: SELECT latest, last 30 readings, 1-hour stats
    D-->>F: rows
    F-->>U: rendered dashboard + chart
```

## 2.3 Edge analytics rule — flowchart

```mermaid
flowchart TD
    A["Read one line from serial port"] --> B{"Line starts with 'T:'?"}
    B -- No --> A
    B -- Yes --> C["Parse temperature (T) and door/tilt (D)"]
    C --> D["Fetch settings row from MariaDB"]
    D --> E{"fan_override"}
    E -- AUTO --> F{"temperature > threshold?"}
    F -- Yes --> G["fan_on = true"]
    F -- No --> H["fan_on = false"]
    E -- ON --> G
    E -- OFF --> H
    G --> I{"alarm_override"}
    H --> I
    I -- AUTO --> J{"door_tilt == 1?"}
    J -- Yes --> K["alarm_on = true"]
    J -- No --> L["alarm_on = false"]
    I -- ON --> K
    I -- OFF --> L
    K --> M{"state changed since last cycle?"}
    L --> M
    M -- Yes --> N["Send 'FAN:..' / 'ALARM:..' command to Arduino"]
    M -- No --> O["Skip command (avoid spamming serial)"]
    N --> P["INSERT reading row into MariaDB"]
    O --> P
    P --> A
```

## 2.4 Technology stack

| Layer | Technology | Reason |
|---|---|---|
| IoT Node firmware | C++ (Arduino core) | Direct, low-level control of ADC and GPIO pins; standard for UNO |
| Node ⇄ Edge link | USB serial, plain-text protocol, 9600 baud | Simple to debug with Serial Monitor; no extra hardware (Wi-Fi/BLE modules) needed |
| Edge runtime | Python 3 (`pyserial`, `mysql-connector-python`) | Readable, fast to prototype, good DB/serial libraries |
| Database | MariaDB (MySQL-compatible) | Matches the assignment's recommended client; relational schema fits fixed-shape sensor rows |
| Dashboard | Flask + Jinja2 + Chart.js | Lightweight web server suitable for a Pi; Chart.js gives a live-updating line chart with minimal code |
