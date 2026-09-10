# 3. Bill of Materials & Wiring Guide

This is the exact circuit for **Smart Room Guardian**, built entirely from
parts found in a standard Arduino UNO R3 starter kit. Follow it in order —
each section is one self-contained sub-circuit. Share a photo after each
section and I can check it before you move on.

## 3.1 Bill of materials

| # | Component | Qty | Role |
|---|---|---|---|
| 1 | Arduino UNO R3 | 1 | Microcontroller / IoT Node |
| 2 | USB-A to USB-B cable | 1 | Power + serial link to the Pi/VM |
| 3 | Breadboard | 1 | Prototyping |
| 4 | 10 kΩ NTC thermistor | 1 | **Analog sensor** — temperature |
| 5 | 10 kΩ resistor | 1 | Voltage-divider partner for the thermistor |
| 6 | Tilt switch (ball-type, e.g. SW-520D) | 1 | **Digital sensor** — door/disturbance |
| 7 | 1-channel 5 V relay module | 1 | **Actuator 1** — fan/appliance switch |
| 8 | Active buzzer | 1 | **Actuator 2** — alarm |
| 9 | LED (any colour) | 1 | Load switched by the relay (stands in for a real fan/appliance) |
| 10 | 220 Ω resistor | 1 | Current-limits the LED load |
| 11 | Jumper wires (M-M, M-F) | ~15 | Wiring |

> **Don't have a thermistor?** Substitute an LM35 analog temperature IC or
> even the photoresistor (LDR) with a fixed resistor divider — any analog
> sensor satisfies the "1 analog sensor" requirement. The Arduino sketch has
> a `#define SENSOR_LM35` switch ready for this (see
> [docs/04](04-arduino-node.md)). Wiring below assumes the thermistor.

## 3.2 Pin map (reference table)

| Arduino pin | Connects to | Direction |
|---|---|---|
| `A0` | Thermistor / 10 kΩ divider midpoint | Analog input |
| `D2` | Tilt switch (other leg → GND) | Digital input, `INPUT_PULLUP` |
| `D8` | Relay module `IN` | Digital output |
| `D9` | Buzzer `+` | Digital output |
| `5V` | Breadboard `+` rail, relay `VCC`, thermistor top | Power |
| `GND` | Breadboard `−` rail, relay `GND`, buzzer `−`, tilt switch leg | Ground |
| `D13` | *(no wiring needed)* | Onboard LED, used as a "heartbeat" |

## 3.3 Step 1 — power rails

1. Plug the Arduino's `5V` pin into the breadboard's red (`+`) rail.
2. Plug the Arduino's `GND` pin into the breadboard's blue/black (`−`) rail.
3. Every component below gets its power and ground from these two rails,
   not directly from the Arduino pins — this keeps wiring tidy and is
   standard breadboard practice.

## 3.4 Step 2 — temperature sensor (analog, voltage divider)

The thermistor's resistance changes with temperature; we read it as a
voltage using a divider against a fixed 10 kΩ resistor.

1. Place the thermistor on the breadboard, one leg in row *n*, the other in
   row *m* (any two separate rows).
2. Wire thermistor leg 1 → breadboard `+` rail (5V).
3. Place the 10 kΩ resistor: one leg into the **same row** as thermistor
   leg 2, the other leg → breadboard `−` rail (GND).
4. From the **shared row** (thermistor leg 2 + resistor leg 1), run a jumper
   to Arduino `A0`.

This creates: `5V → thermistor → A0 (midpoint) → 10kΩ resistor → GND`. As
temperature rises, the thermistor's resistance falls, so the voltage at A0
rises. (Component has no polarity — either leg either way is fine.)

## 3.5 Step 3 — door/tilt sensor (digital)

1. Place the tilt switch on the breadboard.
2. Wire one leg → Arduino `D2`.
3. Wire the other leg → breadboard `−` rail (GND).
4. No external resistor needed — the sketch enables the Arduino's internal
   pull-up resistor on `D2` in software (`INPUT_PULLUP`). At rest the pin
   reads HIGH; when the switch's internal ball breaks the contact it reads
   LOW (or vice-versa depending on which way you tilt it — either state
   transition is what the sketch treats as "triggered").

## 3.6 Step 4 — buzzer (actuator 1: alarm)

1. Note the buzzer's `+` leg (usually the longer leg, or marked with a `+`
   / a coloured wire on breakout modules).
2. Wire `+` → Arduino `D9`.
3. Wire `−` → breadboard `−` rail (GND).

## 3.7 Step 5 — relay module + LED load (actuator 2: fan/appliance)

The relay module has two sides: a **control side** (3 pins: `VCC`, `GND`,
`IN`) driven by the Arduino, and a **switched side** (3 screw terminals:
`COM`, `NO`, `NC`) which is an electrically isolated mechanical switch.

**Control side:**
1. `VCC` → breadboard `+` rail (5V).
2. `GND` → breadboard `−` rail (GND).
3. `IN` → Arduino `D8`.

**Switched side — drives the LED "fan" load:**
1. `COM` (common) → breadboard `+` rail (5V).
2. `NO` (normally open) → one leg of the 220 Ω resistor.
3. Other leg of the 220 Ω resistor → LED anode (longer leg).
4. LED cathode (shorter leg, flat edge on the LED body) → breadboard `−`
   rail (GND).

When the sketch sets `D8` HIGH, the relay's internal switch closes the
`COM`–`NO` contact, completing the LED's circuit — this is your "fan turned
on" indicator. Using `NO` means the load is off by default (safe state) and
only turns on when commanded.

> ⚠️ **Safety note:** only ever wire the relay's switched side to the 5V
> breadboard rail and an LED, as above. **Do not** connect the relay to
> mains AC power — this kit and breadboard are not rated for it, and it is
> outside the scope (and safety) of this assignment. The relay's clicking
> sound and the LED lighting up are sufficient to demonstrate the actuator
> working.

## 3.8 Final check before powering on

- [ ] No wire bridges two rows that shouldn't be connected (check against
      the tables above).
- [ ] `+` rail only touches 5V-tolerant pins; `−` rail only touches GND.
- [ ] LED is the right way around (flat edge / short leg → GND side).
- [ ] Buzzer polarity respected.
- [ ] USB cable connects UNO to your laptop/desktop first (not yet the VM)
      to sanity-check the sketch via the Arduino IDE Serial Monitor before
      wiring the VM into the loop — see [docs/04](04-arduino-node.md).

Once wired, move on to [docs/04 — Arduino node walkthrough](04-arduino-node.md)
to upload the sketch and verify each sensor/actuator individually.
