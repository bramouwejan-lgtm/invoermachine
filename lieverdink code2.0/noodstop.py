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
    
    controller.set_relay(0, False)
    controller.set_relay(1, False)
    controller.set_relay(2, False)
    controller.set_relay(3, False)
    controller.set_relay(4, False)
    controller.set_relay(6, False)
    controller.set_relay(7, False)
    controller.stop_stappenmotor()
    controller.first_cycle = True
    
    while True:
        # Controleer of noodstopknop nog wordt ingedrukt
        if not controller.btn_noodstop_pushed():
            print ("Noodstop knop losgelaten")
            print ("terug naar rust")
            time.sleep(0.2)
            controller.first_cycle = True
            break
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is noodstop loop nummer ", loopnummer)
    controller.set_relay(5, False)      #rood lampje uit
    # Zorg dat de knopstatus wordt gereset voor de hoofdlus in rust2.py
    controller.button_noodstop_pressed = False
