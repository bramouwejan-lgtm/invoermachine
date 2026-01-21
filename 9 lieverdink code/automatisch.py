import RPi.GPIO as GPIO
import time
import reset
import bufferleeg
import noodstop
import handmatig

def automatisch(controller):
    print ("automatische stand bereikt!")
    loop = 0
    loopnummer = 0
    controller.set_relay(6, True)               #groene lamp is aan
    controller.lift_omhoog(allow_in_automatisch=True)  #lift om hoog (met veiligheidschecks)
    
    while loop == 0:
        
        # stopknop is ingedrukt            
        if controller.btn_stop_pushed():
            print ("terug naar rust")
            time.sleep(0.2)
            loop = 1                            #naar rust

        # handmatige knop is ingedrukt
        elif controller.btn_handmatig_pushed():
            print ("Naar handmatige stand!")
            time.sleep(0.2)
            controller.set_relay(6, False)      #groene lamp is uit
            handmatig.handmatig(controller)     # Naar handmatige stand
            loop = 1                            #naar rust

        # reset knop is ingedrukt    
        elif controller.btn_reset_pushed():
            print ("Naar reset stand!")
            controller.set_relay(6, False)      #groene lamp is uit
            reset.reset(controller)         #naar reset
            loop = 1                        #naar rust
            
        # Noodstopknop is ingedrukt
        elif controller.btn_noodstop_pushed():
            print ("Opstarten NOODSTOP stand")
            time.sleep(0.2)
            noodstop.noodstop(controller)   #naar Noodstop
            loop = 1                        #naar rust
            print("terug naar rust")
            
        # de buffer is leeg     
        elif controller.sensor_boven_lift_active(): 
            controller.lift_stop()                   # lift stop
            print ("buffer is leeg")
            time.sleep(0.2)
            bufferleeg.bufferleeg(controller)       #naar bufferleeg
            loop = 1                                #naar rust

        # de lift staat in de goede posietie om een plank te duwen
        elif controller.sensor_plank_active():      # als de lift boven is
            controller.lift_stop()                   # lift stop
            print ("lift is boven")
            print ("klaar om een plank in te voeren")
            time.sleep(0.2)
            loop2 = 0
            
            while loop2 == 0:
                if controller.btn_noodstop_pushed():                        # als de lift wel boven is en er op de noodstopknop wordt gedrukt.
                    print ("Opstarten NOODSTOP stand")
                    time.sleep(0.2)
                    noodstop.noodstop(controller)   #naar noodstop
                    loop2 = 1
                    loop = 1                        #naar rust
                    
                elif controller.sensor_volgende_plank_active():        # als de lift wel boven is en de sensor geeft aan dat er een plank mag komen.
                    time.sleep(1)
                    print("Start stappenmotor: Plank wordt geduwd.")

                    # Stopknop mag tijdens het duwen ingedrukt worden; we onthouden dat,
                    # maar laten eerst de heen- en terugslag afmaken voordat we naar rust gaan.
                    stop_aangevraagd = False
                    noodstop_onderweg = False

                    controller.start_stappenmotor(richting='CW', steps_per_sec=1000)
                    while True:
                        if controller.btn_noodstop_pushed():
                            print("Opstarten NOODSTOP stand")
                            time.sleep(0.2)
                            noodstop.noodstop(controller)
                            noodstop_onderweg = True
                            break
                        if controller.btn_stop_pushed():
                            stop_aangevraagd = True
                        if controller.sensor_einde_active():
                            controller.stop_stappenmotor() # Stop de motor
                            print("Stappenmotor gestopt (einde).")
                            break
                        time.sleep(0.01)

                    # Alleen terug als we niet naar noodstop zijn gegaan
                    if not noodstop_onderweg:
                        time.sleep(0.5)
                        controller.start_stappenmotor(richting='CCW', steps_per_sec=3000) 
                        while True:
                            if controller.btn_noodstop_pushed():
                                print("Opstarten NOODSTOP stand")
                                time.sleep(0.2)
                                noodstop.noodstop(controller)
                                noodstop_onderweg = True
                                break
                            if controller.btn_stop_pushed():
                                stop_aangevraagd = True
                            if controller.sensor_home_active():
                                controller.stop_stappenmotor()
                                print("Stappenmotor gestopt (home).")
                                break
                            time.sleep(0.01)
                            
                    # Stop motor alleen als deze nog actief is (niet al gestopt door noodstop)
                    if not noodstop_onderweg:
                        controller.stop_stappenmotor()

                    if noodstop_onderweg:
                        loop2 = 1
                        loop = 1
                        break

                    loopnummer = loopnummer+1
                    print ("dit is de ", loopnummer, "ste plank")
                    loop2 = 1
                    if stop_aangevraagd:
                        print("Stopknop was ingedrukt: terug naar rust na volledige cyclus.")
                        loop = 1                            #naar rust
                    
                elif controller.btn_stop_pushed():                          # als de lift wel boven is en er op de stopknop wordt gedrukt.
                    print ("terug naar rust")
                    time.sleep(0.2)
                    loop2 = 1
                    loop = 1                            #naar rust
                    
                elif controller.sensor_boven_lift_active():                 # als de lift helemaal boven is
                    print ("sensor hoog buffer")
                    time.sleep(0.2)
                    bufferleeg.bufferleeg(controller)
                    loop2 = 1
                    loop = 1                            #naar rust
                elif controller.btn_handmatig_pushed():
                    print ("Naar handmatige stand!")
                    time.sleep(0.2)
                    controller.set_relay(6, False)           #groene lamp is uit
                    handmatig.handmatig(controller)
                    loop2 = 1
                    loop = 1                        #naar rust
                
                                    
            controller.lift_omhoog(allow_in_automatisch=True)  # lift weer omhoog (met checks)
                     
    controller.set_relay(6, False)              #groene lamp is uit
    controller.lift_stop()                       # lift stop
    


