# 8. Raspbian / VirtualBox Setup Guide

Your setup: Raspbian (Debian 64-bit) running as a VirtualBox VM. The one
thing a VM adds versus a real Raspberry Pi is **USB passthrough** — the
Arduino is plugged into your host PC, so VirtualBox has to be told to hand
that USB device to the guest OS instead of keeping it for the host.

## 8.1 Enable USB passthrough for the Arduino

Your VM's *Details* pane already shows `USB Controller: OHCI, EHCI` with
`0 (0 active)` device filters — that's the controller enabled, but no
device captured yet.

1. **Before** plugging in the Arduino: in VirtualBox Manager, select the VM
   → **Settings → USB**. Confirm "Enable USB Controller" is ticked (it is)
   and either OHCI or EHCI is selected — both work for a UNO, which is a
   USB 2.0 full-speed device.
2. Plug the Arduino into your host PC via USB.
3. Start the VM.
4. With the VM window focused, go to the VM's **Devices → USB** menu (in
   the running VM's window, not the Manager) and click the Arduino entry
   (it will show as something like *"Arduino SA Uno R3 [0001]"* or, on
   clone boards, *"1a86:7523 QinHeng Electronics HL-340"*) to capture it
   into the guest.
5. Alternatively, add a permanent filter so it auto-captures every time:
   **Settings → USB → Add filter (+ icon)** → pick the Arduino from the
   list of currently-attached devices.
6. Inside Raspbian, confirm it arrived: `lsusb` should list an Arduino/CH340
   device, and `ls /dev/tty*` should show a new entry (typically
   `/dev/ttyACM0` for genuine UNOs, `/dev/ttyUSB0` for CH340 clones) that
   wasn't there before you plugged it in.

> If USB passthrough fails silently or the device won't capture, VirtualBox
> may need the **Extension Pack** installed (Host machine → VirtualBox →
> Preferences → Extensions) — required for USB 2.0/3.0 passthrough on some
> VirtualBox versions.

## 8.2 System update and required packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y mariadb-server python3-venv python3-pip git
```

## 8.3 Database

```bash
sudo mysql_secure_installation
```

Before loading the schema, open `edge/db/schema.sql` and change
`CHANGE_ME` to a real password, then apply the same password in
`edge/config.py`. Then:

```bash
sudo mysql -u root -p < edge/db/schema.sql
```

Verify:

```bash
mysql -u iot_user -p iot_project -e "SELECT * FROM settings;"
```

## 8.4 Python environment

```bash
python3 -m venv ~/iot-venv
source ~/iot-venv/bin/activate
pip install -r edge/requirements.txt
```

(Run `source ~/iot-venv/bin/activate` again in any new terminal you open —
it doesn't persist automatically.)

## 8.5 Serial port permissions

Non-root users usually need to be in the `dialout` group to open
`/dev/ttyACM0`/`/dev/ttyUSB0`:

```bash
sudo usermod -aG dialout $USER
```

Then **log out and back in** (or reboot the VM) for the group change to
take effect.

## 8.6 Uploading the sketch from inside the VM

Either install the Arduino IDE on the VM:

```bash
sudo apt install -y arduino
```

...then open it, select **Tools → Board → Arduino Uno**, **Tools → Port →
/dev/ttyACM0** (or whichever port `ls /dev/tty*` showed), and upload
`arduino/smart_room_guardian/smart_room_guardian.ino`.

Or, if you already uploaded it from your host machine (recommended — see
[docs/04](04-arduino-node.md)), you don't need to upload it again from the
VM; the sketch stays on the Arduino's flash memory regardless of which
computer it's plugged into.

## 8.7 Configure and run

Edit `edge/config.py`:

```python
SERIAL_PORT = "/dev/ttyACM0"   # match what ls /dev/tty* showed you
DB_CONFIG = {
    "host": "localhost",
    "user": "iot_user",
    "password": "<the password you set in schema.sql>",
    "database": "iot_project",
}
```

Run the two services in separate terminals (both need the venv active):

```bash
# terminal 1
source ~/iot-venv/bin/activate
python3 edge/iot_edge_service.py

# terminal 2
source ~/iot-venv/bin/activate
python3 edge/app.py
```

Open the Raspbian desktop's browser (Chromium) to `http://localhost:5000`.

## 8.8 Optional: run automatically on boot (systemd)

Two ready-made unit files are provided in `edge/systemd/`. Edit the `User`,
`WorkingDirectory`, and `ExecStart` paths inside them to match your actual
username/paths, then:

```bash
sudo cp edge/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now iot-edge.service iot-dashboard.service
sudo systemctl status iot-edge.service
journalctl -u iot-edge.service -f      # live logs
```

## 8.9 Optional: view the dashboard from your host machine's browser

VM **Settings → Network → Adapter 1 → Advanced → Port Forwarding** → add a
rule: Host Port `5000`, Guest Port `5000` (leave IPs blank). Then browse to
`http://localhost:5000` on your **host** machine while the VM is running.
