# lift.py
import RPi.GPIO as GPIO
import time

# -----------------------------
# GPIO pinnen
# -----------------------------
RELAY_UP = 5
RELAY_DOWN = 6
SENSOR_TOP = 7          # sensor lift boven
SENSOR_POSITION =8      # sensor lift op goede positie
SENSOR_BOTTOM =9        # sensor lift helemaal beneden
LAMP = 19               # lampje bij storing

# -----------------------------
# Setup
# -----------------------------
def setup_gpio():
    """Setup GPIO pins only if not already configured"""
    if GPIO.getmode() is None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_UP, GPIO.OUT)
        GPIO.setup(RELAY_DOWN, GPIO.OUT)
        GPIO.setup(SENSOR_TOP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(SENSOR_POSITION, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(SENSOR_BOTTOM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LAMP, GPIO.OUT)
        
        # Start met motor en lamp uit
        GPIO.output(RELAY_UP, GPIO.LOW)
        GPIO.output(RELAY_DOWN, GPIO.LOW)
        GPIO.output(LAMP, GPIO.LOW)

# Initialize GPIO if not already done
setup_gpio()

# -----------------------------
# Functies
# -----------------------------
def stop_motor():
    GPIO.output(RELAY_UP, GPIO.LOW)
    GPIO.output(RELAY_DOWN, GPIO.LOW)

def lamp_on():
    GPIO.output(LAMP, GPIO.HIGH)

def lamp_off():
    GPIO.output(LAMP, GPIO.LOW)

def move_up():
    setup_gpio()  # Ensure GPIO is set up
    stop_motor()
    GPIO.output(RELAY_UP, GPIO.HIGH)
    print("Lift omhoog...")
    while True:
        if GPIO.input(SENSOR_TOP) == GPIO.HIGH:
            print("Lift bovenaan!")
            stop_motor()
            lamp_on()  # machine kan niks meer tot reset
            break
        if GPIO.input(SENSOR_POSITION) == GPIO.HIGH:
            print("Lift op goede positie!")
            stop_motor()
            break
        time.sleep(0.05)

def move_down():
    setup_gpio()  # Ensure GPIO is set up
    stop_motor()
    GPIO.output(RELAY_DOWN, GPIO.HIGH)
    print("Lift omlaag...")
    while True:
        if GPIO.input(SENSOR_BOTTOM) == GPIO.HIGH:
            print("Lift helemaal beneden!")
            stop_motor()
            break
        time.sleep(0.05)

def cleanup():
    # Alleen opruimen als GPIO nog actief is
    if GPIO.getmode() is None:
        return
    stop_motor()
    lamp_off()
    GPIO.cleanup()
