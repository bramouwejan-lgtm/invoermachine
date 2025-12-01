import RPi.GPIO as GPIO
import time
import reset
import bufferleeg
import noodstop
#from RelayController import RelayController

def handmatig(controller):
    buton_state = controller.btn_handmatig_pushed()
    print ("Handmatige stand bereikt!")
    loop = 0
    loopnummer = 0
    #controller.set_relay(7, True)
    controller.set_relay(0, True)
    
    while loop == 0:    
        if controller.btn_stop_pushed():            # als de lift nog niet open is maar wel op de stopknop wordt gedrukt
            print ("terug naar rust")
            time.sleep(0.2)
            #controller.btn_handmatig_pushed() == 0
            controller.button_handmatig = 0
            loop = 1
            
        elif controller.btn_reset_pushed():         # als de lift nog niet open is maar wel op de reset knop wordt gedrukt
            print ("Naar reset stand!")
            reset.reset(controller)
            loop = 1
            
        elif controller.btn_noodstop_pushed():      # als de lift nog niet open is maar wel op de noodstopknop wordt gedrukt
            print ("Opstarten NOODSTOP stand")
            time.sleep(0.2)
            noodstop.noodstop(controller)
            loop = 1

        elif controller.sensor_plank_active():      # als de lift boven is
            controller.set_relay(0, False)          # moter gaat uit
            controller.set_relay(7, True)           # lamp bij de handmatige knop aan
            print ("lift is boven")
            print ("klaar om een plank in te voeren")
            time.sleep(0.2)
            loop2 = 0
            
            while loop2 == 0:
                
                if controller.btn_noodstop_pushed():                        # als de lift wel boven is en er op de noodstopknop wordt gedrukt.
                    print ("Opstarten NOODSTOP stand")
                    time.sleep(0.2)
                    noodstop.noodstop(controller)
                    loop2 = 1
                    loop = 1
                    
                elif controller.btn_handmatig_pushed()> buton_state:        # als de lift wel boven is en er op de handmatige knop wordt gedrukt.
                    time.sleep(1)
                    loopnummer = loopnummer+1
                    print ("dit is de ", buton_state, "ste plank")
                    buton_state = controller.btn_handmatig_pushed()
                    # code duwen plank komt hier!!!
                    loop2 = 1
                    
                elif controller.btn_stop_pushed():                          # als de lift wel boven is en er op de stopknop wordt gedrukt.
                    print ("terug naar rust")
                    time.sleep(0.2)
                    loop2 = 1
                    loop = 1
                    
                elif controller.sensor_boven_lift_active():                 # als de lift helemaal boven is
                    print ("sensor hoog buffer")
                    time.sleep(0.2)
                    bufferleeg.bufferleeg(controller)
                    loop2= 1
                    loop = 1
                    
            controller.set_relay(7, False)      # lamp bij de handmatige knop uit
            controller.set_relay(0, True)
            
        elif controller.sensor_boven_lift_active():                         # als de lift helemaal boven is
            print ("sensor hoog buffer")
            time.sleep(0.2)
            bufferleeg.bufferleeg(controller)
            loop = 1
    controller.set_relay(0, False)
    #controller.set_relay(7, False)

