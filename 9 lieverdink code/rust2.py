#!/usr/bin/env python3
import time
from RelayController import RelayController
import automatisch
import handmatig
import reset
import bufferleeg
import noodstop
import RPi.GPIO as GPIO
import traceback

# Laat RelayController zelf de PWM op STEP_PIN aanmaken en beheren
controller = RelayController()
print("Script gestart")
try:
    print("Script gestart")
    print("Wacht op knopdruk...")
    time.sleep(0.1)
    controller.first_cycle = True
    
    while True:
        #print("first cycle is " controller.first_cycle)
        if controller.first_cycle == True:                     #dit zorgt er voor dat de eerste cycle de stappenmotor goed staat.
            if controller.sensor_home_active():
                print ("Stappenmotor staat goed")
                controller.first_cycle = False
            elif controller.btn_noodstop_pushed():
                print ("Opstarten NOODSTOP stand")
                time.sleep(0.05)
                noodstop.noodstop(controller)
            elif not controller.sensor_home_active():
                controller.start_stappenmotor(richting='CCW', steps_per_sec=1000)
                print ("stappenmotor nog niet op de juiste positie")
                timeout_counter = 0
                max_timeout = 300  # Max 30 seconden (300 * 0.1s)
                
                while not controller.sensor_home_active():
                    if controller.btn_noodstop_pushed():
                        print ("Opstarten NOODSTOP stand")
                        time.sleep(0.05)
                        controller.stop_stappenmotor()
                        noodstop.noodstop(controller)
                        controller.start_stappenmotor(richting='CCW', steps_per_sec=1000)
                        timeout_counter = 0  # Reset timeout bij noodstop
                        continue
                    elif controller.sensor_home_active():
                        controller.stop_stappenmotor()
                        break
                    
                    # Timeout check om oneindige loop te voorkomen
                    timeout_counter += 1
                    if timeout_counter >= max_timeout:
                        print("WAARSCHUWING: Timeout bij homing stappenmotor!")
                        controller.stop_stappenmotor()
                        break
                    time.sleep(0.1)
                    
                controller.stop_stappenmotor()
                controller.first_cycle = False
            
        
        # Noodstop heeft absolute prioriteit (NO knop): direct naar noodstop en daarna weer bovenaan de while landen.
        if controller.btn_noodstop_pushed():
            print ("Opstarten NOODSTOP stand")
            time.sleep(0.05)
            noodstop.noodstop(controller)
            continue

        if controller.btn_start_pushed():
            print ("Opstarten automatische stand.")
            time.sleep(0.2)

            # Oude stop-druk uit rust niet meenemen de automatische stand in
            controller.btn_stop_pushed()  # reset eventueel opgeslagen stop-flag

            automatisch.automatisch(controller)

            # Reset eventuele handmatige knopdruk die tijdens automatisch is opgeslagen
            controller.btn_handmatig_pushed()
                
        elif controller.btn_reset_pushed():
            print ("Opstarten reset modus")
            time.sleep(0.2)
            reset.reset(controller)
            
        elif controller.sensor_boven_lift_active():
            print ("sensor hoog buffer")
            time.sleep(0.2)
            bufferleeg.bufferleeg(controller)
            

        time.sleep(0.2)
        #controller.button_handmatig_pressed = 0
        
except Exception as e:
    print("FOUT OPGETREDEN:", e)
    traceback.print_exc()
    # Wacht even zodat de foutmelding zichtbaar is
    print("Script wordt afgesloten in 10 seconden...")
    try:
        time.sleep(10)
    except:
        pass    

except KeyboardInterrupt:
    controller.lift_stop()  # stop lift (veilig)
    controller.set_relay(2, False)
    controller.set_relay(3, False)
    controller.set_relay(4, False)
    controller.set_relay(5, False)
    controller.set_relay(6, False)
    controller.set_relay(7, False)
    
    print("Afsluiten...")
finally:
    del controller  # Roept __del__ aan → cleanup
