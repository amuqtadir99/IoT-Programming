"""
Shared configuration for the edge service and the dashboard.

Edit SERIAL_PORT and DB_CONFIG['password'] for your setup before running
anything — see docs/08-raspbian-vm-setup-guide.md.
"""

# Find this with `ls /dev/tty*` before and after plugging in the Arduino.
# Common values: "/dev/ttyACM0" (UNO with genuine ATmega16U2) or
# "/dev/ttyUSB0" (clone boards with a CH340 USB chip).
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

DB_CONFIG = {
    "host": "localhost",
    "user": "iot_user",
    "password": "CHANGE_ME",  # must match edge/db/schema.sql
    "database": "iot_project",
}
