import RPi.GPIO as GPIO
import time
import noodstop
#from RelayController import RelayController
def reset(controller):
    controller.set_relay(0, False)
    print ("reset stand bereikt!")
    loop = 0
    loopnummer = 0
    controller.lift_omlaag(allow_in_reset=True)  # lift omlaag (met veiligheidschecks)
    while loop == 0:
        if controller.btn_stop_pushed():
            print ("terug naar rust")
            time.sleep(0.2)
            loop = 1
            
        elif controller.sensor_onder_lift_active():
            print ("lift is beneden")
            print ("nu is het tijd om de buffer te vullen")
            time.sleep(0.2)
            loop2 = 0
            controller.lift_stop()  # lift stop
            while loop2 == 0:
                if controller.btn_noodstop_pushed():
                    print ("Opstarten NOODSTOP stand")
                    time.sleep(0.2)
                    noodstop.noodstop(controller)
                    loop2 = 1
                elif controller.btn_stop_pushed():
                    print ("terug naar rust")
                    time.sleep(0.2)
                    loop2 = 1
                else:
                    time.sleep(1)
                    loopnummer = loopnummer+1
                    print ("dit is de ", loopnummer, " loop")
            loop = 1
            
        elif controller.btn_noodstop_pushed():
            print ("Opstarten NOODSTOP stand")
            time.sleep(0.2)
            noodstop.noodstop(controller)
            loop = 1
            
        else:
            time.sleep(1)
            loopnummer = loopnummer+1
            print ("dit is de reset ", loopnummer, " loop")
            
    controller.lift_stop()  # lift stop


