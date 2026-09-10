/*
  Smart Room Guardian — IoT Node
  SWE30011 IoT Programming — Assignment 2

  Reads a temperature sensor (analog) and a door/tilt switch (digital),
  reports both over USB serial to the Raspberry Pi edge device, and obeys
  serial commands from the edge device to drive two actuators: a relay
  (fan/appliance) and a buzzer (alarm).

  Wiring: see docs/03-bill-of-materials-and-wiring.md
  Serial protocol: see docs/05-serial-protocol.md

  Node -> Edge (every SEND_INTERVAL_MS):
      "T:<temperature_c>,D:<0|1>\n"

  Edge -> Node commands (one per line):
      "FAN:ON" | "FAN:OFF"
      "ALARM:ON" | "ALARM:OFF"
      "PING"                      -> Node replies "PONG"
*/

// ---- Sensor type selection -------------------------------------------
// Most UNO starter kits ship a 10k NTC thermistor (used with a 10k series
// resistor as a voltage divider). If your kit instead has an LM35 analog
// temperature IC, comment the NTC line and uncomment the LM35 line.
#define SENSOR_NTC_THERMISTOR
// #define SENSOR_LM35

// ---- Pin map (see docs/03) --------------------------------------------
const uint8_t PIN_TEMP_SENSOR = A0;  // analog sensor
const uint8_t PIN_TILT_SWITCH = 2;   // digital sensor (INPUT_PULLUP)
const uint8_t PIN_RELAY_FAN   = 8;   // actuator 1: relay -> fan/appliance
const uint8_t PIN_BUZZER      = 9;   // actuator 2: buzzer -> alarm
const uint8_t PIN_STATUS_LED  = 13;  // onboard LED, heartbeat indicator

// ---- Thermistor constants (10k NTC, beta=3950, 10k series resistor) --
const float SERIES_RESISTOR       = 10000.0;
const float NOMINAL_RESISTANCE    = 10000.0;
const float NOMINAL_TEMPERATURE_C = 25.0;
const float B_COEFFICIENT         = 3950.0;

// ---- Timing -------------------------------------------------------------
const unsigned long SEND_INTERVAL_MS = 2000;  // how often we report to the edge
const unsigned long DEBOUNCE_MS      = 200;   // tilt switch debounce window

unsigned long lastSendTime      = 0;
unsigned long lastTiltChangeTime = 0;
int lastTiltReading  = HIGH;
int stableTiltState  = HIGH;

void setup() {
  Serial.begin(9600);

  pinMode(PIN_TILT_SWITCH, INPUT_PULLUP);
  pinMode(PIN_RELAY_FAN, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_STATUS_LED, OUTPUT);

  digitalWrite(PIN_RELAY_FAN, LOW);
  digitalWrite(PIN_BUZZER, LOW);

  lastTiltReading = digitalRead(PIN_TILT_SWITCH);
  stableTiltState  = lastTiltReading;
}

float readTemperatureC() {
#if defined(SENSOR_NTC_THERMISTOR)
  int raw = analogRead(PIN_TEMP_SENSOR);
  if (raw <= 0) raw = 1;  // avoid divide-by-zero on a floating pin
  float resistance = SERIES_RESISTOR / ((1023.0 / raw) - 1.0);

  float steinhart = resistance / NOMINAL_RESISTANCE;
  steinhart = log(steinhart);
  steinhart /= B_COEFFICIENT;
  steinhart += 1.0 / (NOMINAL_TEMPERATURE_C + 273.15);
  steinhart = 1.0 / steinhart;
  steinhart -= 273.15;
  return steinhart;
#elif defined(SENSOR_LM35)
  int raw = analogRead(PIN_TEMP_SENSOR);
  float voltage = raw * (5.0 / 1023.0);
  return voltage * 100.0;  // LM35: 10 mV per degree C
#endif
}

// Debounced digital read: returns 1 while the switch is in its "triggered"
// state (contact pulled to GND) for longer than DEBOUNCE_MS, else 0.
int readTiltDebounced() {
  int reading = digitalRead(PIN_TILT_SWITCH);

  if (reading != lastTiltReading) {
    lastTiltChangeTime = millis();
  }
  if ((millis() - lastTiltChangeTime) > DEBOUNCE_MS) {
    stableTiltState = reading;
  }
  lastTiltReading = reading;

  return (stableTiltState == LOW) ? 1 : 0;
}

void applyCommand(String cmd) {
  cmd.trim();
  if (cmd == "FAN:ON") {
    digitalWrite(PIN_RELAY_FAN, HIGH);
  } else if (cmd == "FAN:OFF") {
    digitalWrite(PIN_RELAY_FAN, LOW);
  } else if (cmd == "ALARM:ON") {
    digitalWrite(PIN_BUZZER, HIGH);
  } else if (cmd == "ALARM:OFF") {
    digitalWrite(PIN_BUZZER, LOW);
  } else if (cmd == "PING") {
    Serial.println("PONG");
  }
}

void loop() {
  // 1. Obey any pending command from the edge device.
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    applyCommand(line);
  }

  // 2. Always sample the tilt switch so debounce timing stays accurate.
  int tilt = readTiltDebounced();

  // 3. Report to the edge device on a fixed interval (non-blocking).
  unsigned long now = millis();
  if (now - lastSendTime >= SEND_INTERVAL_MS) {
    lastSendTime = now;
    float tempC = readTemperatureC();

    Serial.print("T:");
    Serial.print(tempC, 2);
    Serial.print(",D:");
    Serial.println(tilt);

    digitalWrite(PIN_STATUS_LED, !digitalRead(PIN_STATUS_LED));  // heartbeat
  }
}
