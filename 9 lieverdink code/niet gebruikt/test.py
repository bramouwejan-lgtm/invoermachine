import serial
import time
from comhandeler import motor_forward, motor_backward, motor_stop, motor_home

# Open seriële poort naar Arduino (TX van Pi = GPIO14)
# Gebruik serial0 voor meer compatibiliteit
conn = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(2)  # wacht tot Arduino klaar is

print("Raspberry Pi JSON test gestart...")

time.sleep(1)
motor_forward(conn, 1000)
time.sleep(1)

motor_backward(conn, 500)
time.sleep(1)

motor_stop(conn)
time.sleep(1)

motor_home(conn)

conn.close()
print("Test afgerond.")
