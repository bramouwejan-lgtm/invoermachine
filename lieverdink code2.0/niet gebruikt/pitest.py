import serial
import time

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)

test_message = b"Hello Pi loopback!\n"
ser.write(test_message)
time.sleep(1)

received = ser.readline().decode('utf-8').strip()
print(f"Verzonden: {test_message.decode('utf-8').strip()}")
print(f"Ontvangen: {received}")

ser.close()
