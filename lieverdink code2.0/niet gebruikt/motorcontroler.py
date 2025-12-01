import RPi.GPIO as GPIO
import time
from RelayController import RelayController
controller = RelayController()
def Lift_omhoog(controller):
    print ("lift omhoog")
    loop = 0
    loopnummer = 0
    controller.set_relay(0, True)
    while loop == 0:
        if controller.sensor_boven_lift_active():
            print ("lift is helemaal boven")
            time.sleep(0.2)
            loop = 1
        elif controller.sensor_plank_active():
            print ("plank staat klaar")
            time.sleep(0.2)
            loop = 1
        
        elif controller.btn_noodstop_pushed():
            print ("NOODSTOP ingedrukt")
            time.sleep(0.2)
            loop = 1
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is de ", loopnummer, " loop")

    controller.set_relay(0, False)

def Lift_omlaag(controller):
    print ("lift omlaag")
    loop = 0
    loopnummer = 0
    controller.set_relay(1, True)
    while loop == 0:
        if controller.sensor_onder_lift_active():
            print ("terug naar rust")
            time.sleep(0.2)
            loop = 1
        elif controller.btn_noodstop_pushed():
            print ("NOODSTOP ingedrukt")
            time.sleep(0.2)
            loop = 1
        elif controller.btn_stop_pushed():
            print ("terug naar rust")
            time.sleep(0.2)
            loop = 1
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is de ", loopnummer, " loop")

    controller.set_relay(1, False)

#try: 
#    print("Wacht op knopdruk...")
#    while True:
#        if controller.btn_reset_pushed():
#            Lift_omlaag(controller)
#        elif controller.btn_start_pushed():
#            Lift_omhoog(controller)
#        time.sleep(0.2)

#except KeyboardInterrupt:
#    print("Afsluiten...")
#finally:
#    del controller  # Roept __del__ aan → cleanup
