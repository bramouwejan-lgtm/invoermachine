# rust.py
import RPi.GPIO as GPIO
import time
import subprocess  # om andere scripts te starten
from stappen_motor import go_home

# ------------------------------
# GPIO-pinnen (pas aan naar je eigen setup)
# ------------------------------
STEPS_PIN = 18       # Stappenmotor pulse pin
DIR_PIN = 23         # Stappenmotor richting pin
HOME_SENSOR = 17     # Home positie sensor (HIGH wanneer home)
START_BUTTON = 3    # Start knop
RESET_BUTTON = 6    # Reset knop
EMERGENCY_BUTTON = 16   # nootstop knop (verplaatst om conflicten te vermijden)
GROENE_LAMP_PIN = 8     # Signaal lamp 

# ------------------------------
# GPIO setup
# ------------------------------
GPIO.setmode(GPIO.BCM)

# Stappenmotor pins
GPIO.setup(STEPS_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Sensor, knoppen en lampen
GPIO.setup(HOME_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # knop naar GND
GPIO.setup(RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # knop naar GND
GPIO.setup(EMERGENCY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # knop naar GND
GPIO.setup(GROENE_LAMP_PIN, GPIO.OUT)


# ------------------------------
# Functie: stappenmotor pulse geven
# ------------------------------
def step_motor(pulses=1, delay=0.001):
    for _ in range(pulses):
        GPIO.output(STEPS_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEPS_PIN, GPIO.LOW)
        time.sleep(delay)


# ------------------------------
# Functie: wachten op knop
# ------------------------------
def wait_for_button():
    print("Wachten op knopdruk (start of reset)...")
    while True:
        if GPIO.input(START_BUTTON) == GPIO.LOW:            # pin 3
            print("Startknop ingedrukt! Overschakelen naar automatisch.py")
            GPIO.output(GROENE_LAMP_PIN, GPIO.LOW)
            GPIO.cleanup()
            time.sleep(0.1)  # Small delay to ensure GPIO cleanup is complete
            subprocess.run(["python3", "/home/bram/project/automatisch.py"])
            break
        if GPIO.input(RESET_BUTTON) == GPIO.LOW:            # pin 6
            print("Resetknop ingedrukt! Overschakelen naar reset.py")
            GPIO.output(GROENE_LAMP_PIN, GPIO.LOW)
            GPIO.cleanup()
            time.sleep(0.1)  # Small delay to ensure GPIO cleanup is complete
            subprocess.run(["python3", "/home/bram/project/reset.py"])
            break
        if GPIO.input(EMERGENCY_BUTTON) == GPIO.LOW:        # pin 24
            print("Noodstop ingedrukt! Start nootstop script")
            GPIO.output(GROENE_LAMP_PIN, GPIO.LOW)
            GPIO.cleanup()
            time.sleep(0.1)  # Small delay to ensure GPIO cleanup is complete
            subprocess.run(["python3", "/home/bram/project/nootstop.py"])
            break
        time.sleep(0.1)

# ------------------------------
# Hoofdprogramma
# ------------------------------
try:
    print("Rust stand bereikt!")
    GPIO.output(GROENE_LAMP_PIN, GPIO.HIGH)
    go_home()
    wait_for_button()
finally:
    if GPIO.getmode() is not None:
        GPIO.output(GROENE_LAMP_PIN, GPIO.LOW)
        GPIO.cleanup()
