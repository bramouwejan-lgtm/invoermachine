import serial
import time

# Open seriële poort (UART van de Pi)
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)  # even wachten tot Arduino klaar is

# Verstuur bericht
message = "Hallo\n"
ser.write(message.encode('utf-8'))
print(f"Verstuurd: {message.strip()}")

ser.close()
