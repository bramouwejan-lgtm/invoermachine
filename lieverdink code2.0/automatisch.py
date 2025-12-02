import RPi.GPIO as GPIO
import time
import reset
import bufferleeg
import noodstop
from stappenmotorcontroler_nieuw import stappenmotorcontroler_nieuw
#from stappen_motor import stappen_motor
#from RelayController import RelayController

def automatisch(controller):
    print ("automatische stand bereikt!")
    loop = 0
    loopnummer = 0
    controller.set_relay(6, True)               #groene lamp is aan
    controller.set_relay(0, True)
    
    while loop == 0:
        if controller.btn_stop_pushed():
            print ("terug naar rust")
            time.sleep(0.2)
            loop = 1
            
        elif controller.btn_handmatig_pushed() >0:
            print ("Naar handmatige stand!")
            time.sleep(0.2)
            loop = 1
            
        elif controller.btn_reset_pushed():
            print ("Naar reset stand!")
            reset.reset(controller)
            loop = 1
            
        elif controller.btn_noodstop_pushed():
            print ("Opstarten NOODSTOP stand")
            time.sleep(0.2)
            noodstop.noodstop(controller)
            loop = 1
            
        elif controller.sensor_boven_lift_active():
            controller.set_relay(0, False)          # moter gaat uit
            print ("sensor hoog buffer")
            time.sleep(0.2)
            bufferleeg.bufferleeg(controller)
            loop = 1
            
        elif controller.sensor_plank_active():      # als de lift boven is
            controller.set_relay(0, False)          # moter gaat uit
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
                    
                elif controller.sensor_volgende_plank_active():        # als de lift wel boven is en de sensor geeft aan dat er een plank mag komen.
                    time.sleep(1)
                    print("Start stappenmotor: Plank wordt geduwd.")
                    
                    # Gebruik 'CW' of 'CCW' voor de richting die de plank duwt ('vooruit')
                    controller.start_stappenmotor(richting='CW', steps_per_sec=1000)
                    while True:
                        if controller.sensor_einde_active():
                            controller.stop_stappenmotor() # Stop de motor
                            print("Stappenmotor gestopt.")
                            break
                    controller.start_stappenmotor(richting='CCW', steps_per_sec=1000) 
                    time.sleep(0.5) 
                    controller.stop_stappenmotor()
                    # Als je weer de stappenmotorcontroller wilt gebruiken:
                    # lift = stappenmotorcontroler_nieuw(controller)
                    # lift.duwen()
                    loopnummer = loopnummer+1
                    print ("dit is de ", loopnummer, "ste plank")
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
                        
            controller.set_relay(0, True)       # motor is aan
                     
    controller.set_relay(6, False)              #groene lamp is uit


