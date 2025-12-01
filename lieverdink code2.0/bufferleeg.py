import RPi.GPIO as GPIO
import time
import reset
from gpiozero import LED
#from RelayController import RelayController

def bufferleeg(controller):
    print ("de buffer is leeg!")
    loop = 0
    loopnummer = 0
    controller.set_relay(0, False)
    controller.set_relay(1, False)
    controller.set_relay(2, False)
    controller.set_relay(3, False)
    controller.set_relay(4, True)       #Oranje lamp aan
    controller.set_relay(5, False)
    controller.set_relay(6, False)
    controller.set_relay(7, False)

    while loop == 0:
        if controller.btn_reset_pushed():
            print ("naar reset modus!")
            reset.reset(controller)
            time.sleep(0.2)
            loop = 1
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is loop nummer ", loopnummer)
    controller.set_relay(4, False)       #Oranje lamp uit
