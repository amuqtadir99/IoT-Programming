# 4. Arduino Node Walkthrough

Sketch: [`arduino/smart_room_guardian/smart_room_guardian.ino`](../arduino/smart_room_guardian/smart_room_guardian.ino)

## 4.1 Uploading the sketch

1. Install the Arduino IDE (on your laptop first, to test in isolation —
   or directly on the Raspbian VM, see [docs/08](08-raspbian-vm-setup-guide.md)).
2. Open the `.ino` file.
3. `Tools → Board → Arduino Uno`.
4. `Tools → Port → (select the UNO's port)`.
5. Click **Upload**.
6. `Tools → Serial Monitor`, set baud rate to **9600**. You should see lines
   like `T:23.87,D:0` appear every 2 seconds.

Test the sketch here, on your own machine, before ever connecting it to the
Raspbian VM — it's much faster to debug wiring with the IDE's Serial
Monitor than through the Python service.

## 4.2 Code walkthrough

**Sensor selection (`#define`)** — a compile-time switch lets the same
sketch support either a 10 kΩ NTC thermistor (default) or an LM35, since
starter kits vary. Only one of `SENSOR_NTC_THERMISTOR` / `SENSOR_LM35`
should be uncommented at a time.

**`readTemperatureC()`** — for the thermistor, converts the raw ADC value
(0–1023) into a resistance (via the voltage-divider equation), then into a
temperature using the simplified Steinhart–Hart (beta) equation, which is
the standard approach for consumer NTC thermistors and only needs the
thermistor's nominal resistance, nominal temperature, and beta coefficient
(printed on most kit datasheets, otherwise 3950 is a safe default for a 10k
NTC).

**`readTiltDebounced()`** — a tilt switch is a mechanical contact; it can
bounce (rapidly toggle) for a few milliseconds when it changes state. This
function only accepts a new state once it has been stable for
`DEBOUNCE_MS` (200 ms), avoiding false triggers being sent to the edge
device.

**`applyCommand()`** — parses one line of incoming serial text and maps it
directly onto `digitalWrite()` calls for the relay and buzzer pins. Unknown
commands are silently ignored, which keeps the Node robust against a
malformed or partial line from the edge device.

**`loop()`** — deliberately non-blocking: it checks for an incoming command,
updates the debounced tilt reading, and only sends a new report once
`SEND_INTERVAL_MS` has elapsed, using `millis()` instead of `delay()`. This
means the Node can react to an incoming `FAN:ON`/`ALARM:ON` command
immediately, rather than being stuck inside a `delay()` call — important
because actuator commands should be applied as soon as they arrive, not
batched with the next sensor report.

**Heartbeat LED (`D13`)** — toggles every send cycle, a simple visual
confirmation (with no extra wiring, since it's the UNO's built-in LED) that
the loop is alive even without a Serial Monitor attached.

## 4.3 Verifying each part independently (before wiring to the Pi)

With the Serial Monitor open (9600 baud):

- **Thermistor:** warm the thermistor between your fingers — the `T:` value
  should rise within a few seconds.
- **Tilt switch:** tilt the breadboard/switch — the `D:` value should flip
  between `0` and `1`.
- **Relay/LED:** type `FAN:ON` into the Serial Monitor's send box and hit
  Enter — you should hear the relay click and see the LED light up. Type
  `FAN:OFF` to reverse it.
- **Buzzer:** type `ALARM:ON` — the buzzer should sound. Type `ALARM:OFF`
  to silence it.

Once all four behave correctly from the Serial Monitor, the Node is ready
to be handed over to the Python edge service (which sends exactly these
same commands automatically) — see [docs/05](05-serial-protocol.md).
