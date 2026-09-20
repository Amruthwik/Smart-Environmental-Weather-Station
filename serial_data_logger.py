import csv
import serial
from datetime import datetime

SERIAL_PORT = "COM3"
BAUD_RATE = 115200
OUTPUT_FILE = "sensor_data.csv"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

with open(OUTPUT_FILE, "a", newline="") as file:
    writer = csv.writer(file)

    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if not line or line.startswith("#"):
            continue

        parts = [part.strip() for part in line.split(",")]

        if len(parts) == 4:
            writer.writerow([datetime.now().isoformat()] + parts)
            file.flush()
