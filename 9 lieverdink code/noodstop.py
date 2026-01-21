import RPi.GPIO as GPIO
import time
from gpiozero import LED
#from RelayController import RelayController
#controller = RelayController()
def noodstop(controller):
    print ("NOODSTOP berijkt!")
    print ("Stop alle actuatoren!")
    loopnummer = 0
    controller.set_relay(5, True)       #rood lampje aan
    
    controller.lift_stop()  # stop lift (veilig)
    controller.set_relay(2, False)
    controller.set_relay(3, False)
    controller.set_relay(4, False)
    controller.set_relay(6, False)
    controller.set_relay(7, False)
    controller.stop_stappenmotor()
    # Reset first_cycle flag zodat rust2.py weet dat homing nodig kan zijn na noodstop
    if hasattr(controller, 'first_cycle'):
        controller.first_cycle = True
    
    while True:
        # Controleer of noodstopknop nog wordt ingedrukt
        if not controller.btn_noodstop_pushed():
            print ("Noodstop knop losgelaten")
            print ("terug naar rust")
            time.sleep(0.2)
            if hasattr(controller, 'first_cycle'):
                controller.first_cycle = True
            break
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is noodstop loop nummer ", loopnummer)
    controller.set_relay(5, False)      #rood lampje uit
    # Zorg dat de knopstatus wordt gereset voor de hoofdlus in rust2.py
    # Gebruik de publieke methode i.p.v. directe attribuut access
    # (btn_noodstop_pushed() reset zelf al de flag bij loslaten)
