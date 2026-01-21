import RPi.GPIO as GPIO
import time

class stappen_motor:

    def __init__(self, pin_pwm, pin_in1, pin_in2, freq=1000):
        GPIO.setmode(GPIO.BCM)

        self.pin_pwm = pin_pwm
        self.pin_in1 = pin_in1
        self.pin_in2 = pin_in2

        GPIO.setup(pin_in1, GPIO.OUT)
        GPIO.setup(pin_in2, GPIO.OUT)
        GPIO.setup(pin_pwm, GPIO.OUT)

        self.pwm = GPIO.PWM(pin_pwm, freq)
        self.pwm.start(0)   # start met 0% duty cycle

    def forward(self, speed):
        GPIO.output(self.pin_in1, GPIO.HIGH)
        GPIO.output(self.pin_in2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def backward(self, speed):
        GPIO.output(self.pin_in1, GPIO.LOW)
        GPIO.output(self.pin_in2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.pin_in1, GPIO.LOW)
        GPIO.output(self.pin_in2, GPIO.LOW)
