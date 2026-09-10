# 10. Report Writing Guide (rubric-mapped)

Word limit: **2000 ± 10%** (i.e. 1800–2200 words), excluding the appendix
code listing (confirm this against your unit's current wording — word-limit
rules can change between offerings). Write everything below in your own
voice — the docs in this repo are scaffolding, not final prose to copy in.

## 10.1 Suggested word budget

| Section | Words | Source material in this repo |
|---|---|---|
| Summary | 350–450 | [docs/01](01-project-summary.md) |
| Conceptual design | 300–400 (+ diagrams, not counted) | [docs/02](02-conceptual-design.md) |
| Implementation — Sensors | 250–300 | [docs/03](03-bill-of-materials-and-wiring.md), [docs/04](04-arduino-node.md) |
| Implementation — Actuators | 250–300 | [docs/03](03-bill-of-materials-and-wiring.md), [docs/04](04-arduino-node.md) |
| Implementation — Software/libraries | 300–400 | [docs/05](05-serial-protocol.md), [docs/06](06-database-and-analytics.md), [docs/07](07-web-dashboard.md) |
| Resources | list, light word count | this file, §10.4 |
| **Total (excl. appendix)** | **~1800–2000** | |

## 10.2 Section-by-section rubric checklist

**Summary** (rubric: well-defined application incl. IoT node, edge device,
UI) — must explicitly name and describe all three: what the Arduino node
senses/actuates, what the edge device (Pi/VM) computes and stores, what the
UI shows and lets the user do. Don't just describe the topic in the
abstract — describe *your build*.

**Conceptual design** (rubric: diagram + description of hardware, software,
operation) — include at minimum the block diagram from
[docs/02](02-conceptual-design.md); the sequence diagram or rule flowchart
strengthens this further as your "UML-style" diagram. Write 2–3 sentences
per diagram explaining what it shows — don't just paste the diagram.

**Implementation — Sensors:** for *each* sensor (thermistor, tilt switch):
what physical quantity it measures, why that's useful for this
application, which Arduino pin/technique reads it (ADC voltage divider vs
digital pull-up), and how the raw reading is converted to a meaningful
value (Steinhart–Hart equation for the thermistor).

**Implementation — Actuators:** for *each* actuator (relay+LED, buzzer):
what it physically does, why the system needs it (what condition it
responds to), and how it's driven (`digitalWrite` on which pin, triggered
by which serial command from the edge device).

**Implementation — Software/libraries:** name the actual libraries used —
`pyserial` (serial I/O), `mysql-connector-python` (DB access), `Flask` +
Jinja2 (web server/templating), `Chart.js` (client-side charting) — and one
sentence each on *how* you used them (e.g. "pyserial's `Serial.readline()`
blocks until a full line is received, which drives the edge service's main
loop").

**Resources:** list every tutorial/datasheet/Stack Overflow answer/AI tool
you actually consulted, with links, in a consistent citation style (e.g.
IEEE or APA per your unit's expectation). If you used AI assistance (as
you're doing with this repo) to help draft code/docs, disclose that
transparently per Swinburne's academic integrity policy for AI-assisted
work — a one- or two-sentence acknowledgement is standard practice, not a
weakness.

**Appendix:** paste the final versions of `smart_room_guardian.ino`,
`iot_edge_service.py`, `app.py`, and `schema.sql` (all in this repo under
`arduino/` and `edge/`). Keep formatting monospaced/readable.

## 10.3 Diagrams to capture as images

GitHub renders the Mermaid blocks in [docs/02](02-conceptual-design.md)
directly on the repo page — screenshot them, or paste the Mermaid source
into the Mermaid Live Editor to export a PNG/SVG for your Word/PDF report.

## 10.4 Starter resources list (expand with what you actually used)

- Arduino thermistor voltage-divider technique — Adafruit / Arduino
  community NTC thermistor tutorials (Steinhart–Hart beta equation).
- `pyserial` documentation — reading/writing a serial port from Python.
- MariaDB / MySQL documentation — `CREATE TABLE`, `ENUM`, aggregate
  functions (`AVG`, `MIN`, `MAX`).
- Flask documentation — routing, Jinja2 templating, `request.form`.
- Chart.js documentation — line chart configuration.
- Unit materials: Week 2 (basic programming) and Week 3 (edge server
  programming) lab content, as referenced in the assignment brief.

Replace/extend this list with the specific pages you actually read while
building your version.
