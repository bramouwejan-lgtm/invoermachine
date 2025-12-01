import RPi.GPIO as GPIO
import time

class RelayController:
    def __init__(self):
        self.relay_pins = [5, 6, 13, 16, 19, 20, 21, 26]    #5 motor om hoog, 6 moter naar beneden, 13,16,19,20,21,26
        self.button_stop = 22           #stopknop
        self.button_start = 17          #startknop
        self.button_noodstop = 23       #Nootstopknop
        self.button_handmatig = 24      #Handmatigeknop
        self.button_reset = 27          #Resetknop
        #self.sensor_boven_lift = 7      #Sensor lift boven

        self._setup_gpio()
        self.button_stop_pressed = False
        self.button_start_pressed = False
        self.button_noodstop_pressed = False
        self.button_handmatig_pressed = 0
        self.button_reset_pressed = False
        #self.sensor_boven_lift_pressed = False  #
        print("RelayController is geïnitialiseerd.")
        

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)

        # stop button
        GPIO.setup(self.button_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_stop, GPIO.FALLING, callback=self.button_stop_event, bouncetime=300)
       

        # start button
        GPIO.setup(self.button_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_start, GPIO.FALLING, callback=self.button_start_event, bouncetime=300)
       

        # nood button
        GPIO.setup(self.button_noodstop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_noodstop, GPIO.FALLING, callback=self.button_noodstop_event, bouncetime=300)
       

        # handmatig button
        GPIO.setup(self.button_handmatig, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_handmatig, GPIO.FALLING, callback=self.button_handmatig_event, bouncetime=300)
       
        # reset button
        GPIO.setup(self.button_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_reset, GPIO.FALLING, callback=self.button_reset_event, bouncetime=300)

        # sensor
        #GPIO.setup(self.sensor_boven_lift, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #def sensor_boven_lift_event(self, channel):
            #if GPIO.input(channel):
                #print("Sensor ACTIEF (hoog signaal)")
            #else:
                #print("Sensor INACTIEF (laag signaal)")

        #GPIO.add_event_detect(self.sensor_boven_lift_pin, GPIO.BOTH, callback=sensor_event, bouncetime=200) #
       
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)  # Zorg dat alles uit staat bij start
            

    def set_relay(self, channel, state):
        if channel < 0 or channel >= len(self.relay_pins):
            raise ValueError("Ongeldige kanaalindex")
        GPIO.output(self.relay_pins[channel], GPIO.LOW if state else GPIO.HIGH)
        print(f"Relay {channel} {'aan' if state else 'uit'} gezet.")


    def button_stop_event(self, channel):
        self.button_stop_pressed = True
        print('stopknop ingedrukt')
        self.button_handmatig_pressed = 0

    def button_start_event(self, channel):
        self.button_start_pressed = True
        print('startknop ingedrukt')
        self.button_handmatig_pressed = 0

    def button_noodstop_event(self, channel):
        self.button_noodstop_pressed = True
        print('noodknop ingedrukt')


    def button_handmatig_event(self, channel):
        self.button_handmatig_pressed +=1
        print('handmatigknop ingedrukt')

    def button_reset_event(self, channel):
        self.button_reset_pressed = True
        print('resetknop ingedrukt')


    def set_next(self):
        gevonden = 0
        pin_1_state = GPIO.input(self.relay_pins[0])
        
        for pin in range(1, len(self.relay_pins)):
            if GPIO.input(self.relay_pins[pin]) != pin_1_state:
                gevonden = 1
                GPIO.output(self.relay_pins[pin], pin_1_state)
                print("Relay", pin+1, "is", "ON" if pin_1_state == GPIO.LOW else "OFF")
                break
            
        if gevonden == 0:
            GPIO.output(self.relay_pins[0], GPIO.LOW if pin_1_state else GPIO.HIGH) 
            print("Relay 1 is", "ON" if pin_1_state == GPIO.HIGH else "OFF")
            


    def all_off(self):
        for pin in self.relay_pins:
            GPIO.output(pin, GPIO.LOW)
        print("Alle relais zijn uitgeschakeld.")

    def btn_start_pushed(self):
        btn_state = self.button_start_pressed
        self.button_start_pressed = False
        return btn_state
    
    def btn_stop_pushed(self):
        btn_state = self.button_stop_pressed
        self.button_stop_pressed = False
        return btn_state
   
    def btn_noodstop_pushed(self):
        # Controleer of de knop momenteel wordt ingedrukt
        current_state = GPIO.input(self.button_noodstop) == GPIO.LOW
        
        # Alleen resetten als de knop niet meer wordt ingedrukt
        if not current_state and self.button_noodstop_pressed:
            self.button_noodstop_pressed = False
            print('Noodstop knop losgelaten')
        
        return self.button_noodstop_pressed
 
    
    def btn_handmatig_pushed(self):
        #btn_state = self.button_handmatig_pressed
        #self.button_handmatig_pressed = False 
        return self.button_handmatig_pressed
    
    def btn_reset_pushed(self):
        btn_state = self.button_reset_pressed
        self.button_reset_pressed = False
        return btn_state

    def cleanup(self):
        self.all_off()
        GPIO.cleanup()
        print("GPIO cleanup uitgevoerd.")

    def __del__(self):
        self.cleanup()
        print("RelayController object is verwijderd.")
        
if __name__ == "__main__":
    controller = RelayController()
    
    try:
        print("Wacht op knopdruk...")
        while True:
            if controller.btn_pushed():
                # print("Knop ingedrukt! Relay aan.")
                #controller.set_relay(0, True)
                #time.sleep(1)  # Relay blijft 1 seconde aan
                #controller.set_relay(0, False)
                #print("Relay uit.")
                controller.set_next()
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Afsluiten...")
    finally:
        del controller  # Roept __del__ aan → cleanup
    
