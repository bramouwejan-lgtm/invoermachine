import time
from RelayController import RelayController
import automatisch
import handmatig
import reset
import bufferleeg
import noodstop
import RPi.GPIO as GPIO

STEP_PIN = 12  # Zorg dat dit matcht met je klasse
motor_pwm = GPIO.PWM(STEP_PIN, 1000)
motor_pwm.start(50)  # PULSE_DUTY_CYCLE = 50
motor_pwm.ChangeDutyCycle(0)

controller = RelayController(motor_pwm=motor_pwm)
print("Script gestart")
try:
    print("Script gestart")
    print("Wacht op knopdruk...")
    while True:
        if controller.btn_start_pushed():
            print ("Opstarten automatische stand.")
            time.sleep(0.2)
            automatisch.automatisch(controller)

            print(controller.btn_handmatig_pushed())

            if controller.btn_handmatig_pushed() >0:
                print ("Opstarten handmatige stand")
                time.sleep(0.2)
                handmatig.handmatig(controller)
        elif controller.btn_reset_pushed():
            print ("Opstarten reset modus")
            time.sleep(0.2)
            reset.reset(controller)
            
        elif controller.sensor_boven_lift_active():
            print ("sensor hoog buffer")
            time.sleep(0.2)
            bufferleeg.bufferleeg(controller)

        elif controller.btn_noodstop_pushed():
            print ("Opstarten NOODSTOP stand")
            time.sleep(0.2)
            noodstop.noodstop(controller)
            
        time.sleep(0.2)
        controller.button_handmatig_pressed = 0
        
except Exception as e:
    print("FOUT OPGETREDEN:", e)
    traceback.print_exc()
    # Houd het script open om de fout te zien
    input("Druk op Enter om te sluiten...")    

except KeyboardInterrupt:
    controller.set_relay(0, False)
    controller.set_relay(1, False)
    controller.set_relay(2, False)
    controller.set_relay(3, False)
    controller.set_relay(4, False)
    controller.set_relay(5, False)
    controller.set_relay(6, False)
    controller.set_relay(7, False)
    
    print("Afsluiten...")
finally:
    del controller  # Roept __del__ aan → cleanup
