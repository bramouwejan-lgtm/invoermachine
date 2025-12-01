import RPi.GPIO as GPIO
import time

getal = 0

# BCM-modus instellen (gebruik GPIO-nummers)
GPIO.setmode(GPIO.BCM)

# Stel GPIO 2 in als output
GPIO.setup(1, GPIO.OUT)

while getal < 5:
    # Zet de pin hoog (3.3V)
    GPIO.output(2, GPIO.HIGH)
    time.sleep(5)

    # Zet de pin laag (0V)
    GPIO.output(2, GPIO.LOW)
    time.sleep(2)  # korte pauze zodat het knipperen zichtbaar is

    print("Gelukt ", getal, " keer")

    # Verhoog teller
    getal += 1

# Netjes afsluiten
GPIO.cleanup()
