import serial
import time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(2)

for i in range(10):
    ser.write(b"Hello Arduino!\n")
    print("verzonden")
    time.sleep(1)

ser.close()
