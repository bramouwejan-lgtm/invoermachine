"""
Nieuwe Stappenmotor Controller
Gebruikt comhandeler.py voor communicatie met de Meadow
En RelayController voor sensor monitoring
"""

import serial
import time
from comhandeler import send_command, motor_forward, motor_backward, motor_home, motor_stop

class stappenmotorcontroler_nieuw:

    def __init__(self, controller):
        # RelayController instantie doorgeven i.p.v. zelf aanmaken
        self.controller = controller
        # Open seriële poort naar de motorcontroler (TX van Pi = GPIO14)
        # Gebruik serial0 voor meer compatibiliteit
        self.conn = serial.Serial('/dev/serial0', 9600, timeout=1)
        time.sleep(2)  # wacht tot de motorcontroler klaar is
        
    def duwen(self):
        print ("Stappen motor vooruit")
        time.sleep(1)
        motor_forward(self.conn, 1000)       #motor naar voren
        time.sleep(1)
        voor = 0
        while voor == 0:
            
            if self.controller.sensor_einde_active():
                motor_stop(self.conn)        #motor stopt
                time.sleep(1)
                voor = 1
            else:
                print ("stappenmotor nog niet aan het einde.")
                time.sleep(1)
        motor_backward(self.conn, 1000)      #motor naar achter
        time.sleep(1)
        achter =0
        while achter ==0:
            if self.controller.sensor_home_active():
                motor_stop(self.conn)
                time.sleep(1)
                achter = 1
            else:
                print ("stappenmotor nog niet op de home positie.")
                time.sleep(1)
                
        print ("stappen motor is weer op home positie")
    def homen(self):
        print ("stappenmotor homen")
        time.sleep(1)
        motor_forward(self.conn, 20)         #motor naar voren
        time.sleep(1)
        home = 0
        while home < 10:
            if self.controller.sensor_einde_active(): # probleem skip 
                motor_stop(self.conn)
                time.sleep(1)
                home = 10
            else:
                home = home+1
        motor_backward(self.conn, 1000)
        time.sleep(1)
        achter =0
        while achter ==0:
            if self.controller.sensor_home_active():
                motor_stop(self.conn)
                time.sleep(1)
                achter = 1
        print ("stappen motor is weer op home positie")
    def vooruit(self):                                #Extra functie om de motor toch nog naar voren te krijgen
        print ("Stappen motor vooruit")
        time.sleep(1)
        motor_forward(self.conn, 1000)       #motor naar voren
        time.sleep(1)
        voor = 0
        while voor == 0:
            if self.controller.sensor_einde_active():
                motor_stop(self.conn)
                time.sleep(1)
                voor = 1
        print ("de motor is naar voren")
    def achteruit(self):                                  #extra functie om de motor toch nog naar achter te krijgen
        motor_backward(self.conn, 1000)
        time.sleep(1)
        achter =0
        while achter ==0:
            if self.controller.sensor_home_active():
                motor_stop(self.conn)
                time.sleep(1)
                achter = 1
        print ("stappen motor is weer op home positie")

      

