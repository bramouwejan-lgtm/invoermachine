import RPi.GPIO as GPIO
import time
from gpiozero import LED
#from RelayController import RelayController
#controller = RelayController()
def noodstop(controller):
    print ("NOODSTOP berijkt!")
    print ("Stop alle actuatoren!")
    loop = 0
    loopnummer = 0
    controller.set_relay(5, True)       #rood lampje aan
    
    controller.set_relay(1, False)
    controller.set_relay(2, False)
    controller.set_relay(3, False)
    controller.set_relay(4, False)
    controller.set_relay(6, False)
    controller.set_relay(7, False)
    controller.set_relay(0, False)

    
    while loop == 0:
        # Controleer of noodstopknop nog wordt ingedrukt
        if not controller.btn_noodstop_pushed():
            print ("Noodstop knop losgelaten")
            print ("terug naar rust")
            time.sleep(0.2)
            loop = 1
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is loop nummer ", loopnummer)
    controller.set_relay(4, False)      #rood lampje uit
