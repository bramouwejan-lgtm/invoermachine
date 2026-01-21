import RPi.GPIO as GPIO
import time

# Let op: Zorg ervoor dat je de BCM-modus instelt vóórdat je een object aanmaakt.
# GPIO.setmode(GPIO.BCM) 

class stepper_motor_driver: # Nieuwe naam om verwarring te voorkomen

    # pin_step komt overeen met je oude pin_pwm
    # pin_dir komt overeen met je oude pin_in1 (of pin_in2)
    def __init__(self, pin_step, pin_dir, freq=1000):
        
        self.pin_step = pin_step
        self.pin_dir = pin_dir
        
        GPIO.setup(pin_dir, GPIO.OUT)
        GPIO.setup(pin_step, GPIO.OUT)

        # Voor Step/Dir besturing gebruik je PWM om PULSEN te genereren.
        # De Duty Cycle moet typisch 50% zijn (een 'blokgolf').
        self.pwm = GPIO.PWM(pin_step, freq)
        self.pwm.start(50) # Start met 50% Duty Cycle (blokgolf)
        self.pwm.ChangeFrequency(0) # Zet de frequentie (snelheid) initieel op 0

    def set_speed_steps_per_sec(self, steps_per_sec):
        """Stelt de snelheid in door de PWM-frequentie aan te passen."""
        if steps_per_sec > 0:
            # Frequentie is direct de steps_per_sec
            self.pwm.ChangeFrequency(steps_per_sec) 
        else:
            # Zet frequentie op 0 om te stoppen
            self.pwm.ChangeFrequency(1) # Kan niet exact 0 zijn, gebruik 1 en ChangeDutyCycle
            self.pwm.ChangeDutyCycle(0)

    def set_direction(self, direction):
        """Stelt de draairichting in ('CW' of 'CCW')."""
        if direction.upper() == 'CW':
            GPIO.output(self.pin_dir, GPIO.HIGH) # Of LOW, afhankelijk van je driver
        elif direction.upper() == 'CCW':
            GPIO.output(self.pin_dir, GPIO.LOW) # De andere staat

    def move(self, direction, steps_per_sec):
        """Combineert richting en snelheid in één methode."""
        self.set_direction(direction)
        self.set_speed_steps_per_sec(steps_per_sec)
        
    def stop(self):
        """Stopt de motor."""
        self.pwm.ChangeFrequency(1)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        """Stop PWM."""
        self.pwm.stop()
