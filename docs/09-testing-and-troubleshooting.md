# 9. Testing & Troubleshooting Checklist

Run through this before recording your video / submitting — it doubles as
evidence you've met every rubric criterion.

## 9.1 Functional checklist

- [ ] **Analog sensor:** warming the thermistor with your fingers changes
      the `T:` value in the Serial Monitor within a few seconds.
- [ ] **Digital sensor:** tilting the switch flips `D:` between `0` and `1`.
- [ ] **Serial reporting (Node → Edge):** `T:..,D:..` lines appear every 2s
      in either the Arduino Serial Monitor or the `iot_edge_service.py`
      console output.
- [ ] **Serial commands (Edge → Node):** typing `FAN:ON` / `ALARM:ON` into
      the Serial Monitor's send box audibly/visibly triggers the relay/LED
      and buzzer.
- [ ] **Database write:** after `iot_edge_service.py` has been running a
      minute, `SELECT * FROM readings ORDER BY id DESC LIMIT 5;` in the
      `mysql` client shows new rows.
- [ ] **Automatic rule — fan:** warm the thermistor above your configured
      threshold; within ~2s the fan/LED turns on automatically, and
      `readings.fan_state` becomes `1`.
- [ ] **Automatic rule — alarm:** tilt the switch; the buzzer sounds
      automatically and `readings.alarm_state` becomes `1`.
- [ ] **Dashboard loads:** `http://localhost:5000` shows current
      temperature, door state, fan/alarm cards, and a chart with data
      points.
- [ ] **Rule changeable from UI:** change the threshold number and click
      "Save rule" — confirm (via the terminal log or by re-warming the
      thermistor) that the new threshold is used within a few seconds.
- [ ] **Manual override from UI:** click "On"/"Off" for the fan or alarm —
      confirm the physical actuator responds even without the matching
      sensor condition, then click "Auto" to hand control back to the rule.
- [ ] **Analytics panel:** mean/min/max values update as more data
      accumulates (leave it running for a few minutes before checking).

## 9.2 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `PermissionError`/`Permission denied: '/dev/ttyACM0'` | Your user isn't in the `dialout` group | `sudo usermod -aG dialout $USER`, then log out/in |
| `SerialException: could not open port` | Wrong port name, or another program has it open | Check `ls /dev/tty*`; close the Arduino IDE Serial Monitor before running the Python service |
| Arduino not visible in the VM at all (`lsusb` shows nothing new) | USB not passed through | Recapture via VM **Devices → USB** menu, or add a USB filter — see [docs/08 §8.1](08-raspbian-vm-setup-guide.md) |
| `mysql.connector.errors.ProgrammingError: Access denied for user 'iot_user'` | Password mismatch between `schema.sql` and `config.py` | Make sure both files use the identical password, or re-run: `ALTER USER 'iot_user'@'localhost' IDENTIFIED BY '...';` |
| Edge service prints "skipping malformed line" occasionally | Normal — happens once when the Arduino auto-resets on serial connect, cutting off a partial line | No action needed if it's a one-off at startup |
| Dashboard shows `--` everywhere | No rows in `readings` yet | Make sure `iot_edge_service.py` is running and has received at least one `T:..` line |
| Fan/alarm never turns on automatically | Override stuck on `OFF`, or threshold set too high | Click "Auto" on the dashboard for that actuator; check the threshold value |
| Relay clicks but LED doesn't light | LED wired backwards, or in the `NC` terminal instead of `NO` | Check LED orientation (flat edge = cathode = GND side) and that you used the relay's `NO` terminal |
| Chart doesn't render | No internet access from the VM (Chart.js loads from a CDN) | Confirm the VM's NAT adapter has internet; check the browser console for a blocked script |
