import serial
import time

ser = serial.Serial("/dev/ttyAMA10", 9600, timeout=1)

while True:
    msg = "Hello Arduino!"
    ser.write((msg + "\n").encode())
    print("Pi sent:", msg)
    time.sleep(1)
 
