# 7. Web Dashboard

Files: [`edge/app.py`](../edge/app.py), [`edge/templates/index.html`](../edge/templates/index.html), [`edge/static/style.css`](../edge/static/style.css)

## 7.1 What it shows (mapped to task 5)

| Rubric point | Where in the dashboard |
|---|---|
| 5A — hosted on the edge device | Flask's built-in server, run on the Raspbian VM (`app.run(host="0.0.0.0", port=5000)`) |
| 5B — displays project data from the DB | Latest temperature/door/fan/alarm cards, pulled live from `readings` |
| 5C — appropriate visualisation | Chart.js line chart of the last 30 readings + a mean/min/max analytics panel |
| 5D — user can trigger an actuator / change the rule | "Save rule" form (threshold) + Auto/On/Off buttons per actuator |

## 7.2 Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Renders the dashboard: latest reading, 30-point history, 1-hour stats, current settings |
| `/update_threshold` | POST | Updates `settings.temp_threshold` |
| `/override/<actuator>/<state>` | POST | Sets `fan_override`/`alarm_override` to `AUTO`/`ON`/`OFF` |
| `/api/latest` | GET | Returns the latest reading as JSON (handy for testing with `curl`, or extending to an auto-updating widget without a full page reload) |

`actuator` and `state` are validated against a fixed whitelist
(`fan`/`alarm`, `AUTO`/`ON`/`OFF`) before being used to build the SQL
`UPDATE`, so there's no injection risk despite the column name being chosen
dynamically.

## 7.3 The chart

`templates/index.html` pulls the last 30 rows the Flask view already
queried (`history`), turns them into two JSON arrays (timestamps,
temperatures) with Jinja's `tojson` filter, and feeds them to Chart.js
(loaded from a CDN — the VM's NAT network adapter gives it outbound
internet access). The page also does a `setTimeout(() => location.reload(),
10000)` so the chart and cards refresh automatically every 10 seconds
without you needing to press F5 during your demo/video.

## 7.4 Running it

```bash
source ~/iot-venv/bin/activate
python3 edge/app.py
```

Then open **`http://localhost:5000`** in the browser inside the Raspbian
VM. If you'd rather view it from your host machine's browser, add a
VirtualBox NAT port-forwarding rule (VM **Settings → Network → Adapter 1 →
Advanced → Port Forwarding**): Host port `5000` → Guest port `5000`, then
browse to `http://localhost:5000` on the host.

## 7.5 Analytics panel (mean/min/max)

The "Last hour analytics" panel is one SQL query, computed in `app.py`:

```sql
SELECT AVG(temperature) AS avg_t, MIN(temperature) AS min_t,
       MAX(temperature) AS max_t, COUNT(*) AS n
FROM readings
WHERE created_at >= NOW() - INTERVAL 1 HOUR;
```

This directly satisfies the assignment's example of extending the
dashboard with "some analysis on the collected data (i.e., mean or
minimum-maximum)".
