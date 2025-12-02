#import RPi.GPIO as GPIO
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO niet gevonden, MockGPIO wordt gebruikt.")
    from MockGPIO import MockGPIO as GPIO
import time

class RelayController:
    PULSE_DUTY_CYCLE = 50
    _shared_pwm = None  # gedeelde PWM-instantie voor alle RelayControllers

    def __init__(self):
        self.relay_pins = [5, 6, 13, 16, 19, 20, 21, 26]    #5 motor om hoog, 6 moter naar beneden, 13,16,19,20,21,26

        #knoppen
        self.button_stop = 22           #stopknop
        self.button_start = 17          #startknop
        self.button_noodstop = 23       #Nootstopknop
        self.button_handmatig = 24      #Handmatigeknop
        self.button_reset = 27          #Resetknop
        #sensoren
        self.sensor_boven_lift = 18     #Sensor lift bovenaan
        self.sensor_plank = 4           #sensor die de plank ziet
        self.sensor_onder_lift = 3      #sensor lift onderaan was 12
        self.sensor_volgende_plank = 25 #sensor bij de andere machine
        self.sensor_home = 9            #sensor beginpositie stappenmotor
        self.sensor_einde = 10          #sensor eindpositie stappenmotor
        # STAPPENMOTOR PINNEN (12 en 3)
        self.STEP_PIN = 12  # Hardware PWM (Jouw nieuwe STEP-pin)
        self.DIR_PIN = 2    # DIR-pin
        #sensor_home_stappenmotor
        #sensor_begin_stappenmotor

        self._setup_gpio()

        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)

        # PWM slechts één keer per proces aanmaken; daarna hergebruiken
        if RelayController._shared_pwm is None:
            RelayController._shared_pwm = GPIO.PWM(self.STEP_PIN, 1000)  # Creëer het PWM-object
            RelayController._shared_pwm.start(self.PULSE_DUTY_CYCLE)     # Start met 50% Duty Cycle
            RelayController._shared_pwm.ChangeDutyCycle(0)               # Zet de Duty Cycle op 0 om te stoppen

        # Verwijs in deze instantie naar de gedeelde PWM
        self._motor_pwm = RelayController._shared_pwm

        #self._setup_gpio()
        self.button_stop_pressed = False
        self.button_start_pressed = False
        self.button_noodstop_pressed = False
        self.button_handmatig_pressed = 0
        self.button_reset_pressed = False
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

        # sensor boven lift
        GPIO.setup(self.sensor_boven_lift, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_boven_lift, GPIO.BOTH, callback=self.sensor_boven_lift_event, bouncetime=200)

        # sensor plank
        GPIO.setup(self.sensor_plank, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_plank, GPIO.BOTH, callback=self.sensor_plank_event, bouncetime=200)

        # sensor onder lift
        GPIO.setup(self.sensor_onder_lift, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_onder_lift, GPIO.BOTH, callback=self.sensor_onder_lift_event, bouncetime=200)

        # sensor bij de andere machine
        GPIO.setup(self.sensor_volgende_plank, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_volgende_plank, GPIO.BOTH, callback=self.sensor_volgende_plank_event, bouncetime=200)

        # sensor beginpositie stappenmotor
        GPIO.setup(self.sensor_home, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_home, GPIO.BOTH, callback=self.sensor_home_event, bouncetime=200)

        # sensor eindpositie stappenmotor
        GPIO.setup(self.sensor_einde, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_einde, GPIO.BOTH, callback=self.sensor_einde_event, bouncetime=200)
        
        
       
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)  # Zorg dat alles uit staat bij start
            
    def start_stappenmotor(self, richting, steps_per_sec):
        """
        Stuurt de stappenmotor aan.
        Richting: 'CW' of 'CCW'. Snelheid: steps/sec (Frequentie).
        """
        if steps_per_sec <= 0:
            self.stop_stappenmotor()
            return
            
        # 1. Richting instellen
        if richting.upper() == 'CW':
            GPIO.output(self.DIR_PIN, GPIO.HIGH)
        elif richting.upper() == 'CCW':
            GPIO.output(self.DIR_PIN, GPIO.LOW)
            
        # 2. Snelheid (Frequentie) en Pulsuitvoer instellen
        self._motor_pwm.ChangeFrequency(steps_per_sec) 
        self._motor_pwm.ChangeDutyCycle(self.PULSE_DUTY_CYCLE)

    def stop_stappenmotor(self):
        """Stopt de motor door de Duty Cycle op 0 te zetten."""
        self._motor_pwm.ChangeDutyCycle(0)


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

    def sensor_boven_lift_event(self, channel):
        if GPIO.input(channel):
            print('sensor lift boven hoog signaal')
        else:
            print('sensor lift boven laag signaal')
            
    def sensor_plank_event(self, channel):
        if GPIO.input(channel):
            print('de plank staat klaar')
        else:
            print('er is nog geen plank')

    def sensor_onder_lift_event(self, channel):
        if GPIO.input(channel):
            print('sensor lift onder hoog signaal')
        else:
            print('sensor lift onder laag signaal')

    def sensor_volgende_plank_event(self, channel):
        if GPIO.input(channel):
            print('volgende plank mag komen')
        else:
            print('volgende plank mag nog niet komen')

    def sensor_home_event(self, channel):
        if GPIO.input(channel):
            print('de stappenmotor bevind zich op de home positie')
        else:
            print('de stappenmotor bevind zich nog niet op de home positie')

    def sensor_einde_event(self, channel):
        if GPIO.input(channel):
            print('de stappenmotor bevind zich aan het einde')
        else:
            print('de stappenmotor bevind zich niet aan het einde')

    

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

    def sensor_boven_lift_active(self):
        """Controleer of sensor 1 actief is (hoog signaal)"""
        return GPIO.input(self.sensor_boven_lift) == GPIO.HIGH

    def sensor_plank_active(self):
        """Controleer of sensor 1 actief is (hoog signaal)"""
        return GPIO.input(self.sensor_plank) == GPIO.HIGH

    def sensor_onder_lift_active(self):
        """Controleer of sensor 1 actief is (hoog signaal)"""
        return GPIO.input(self.sensor_onder_lift) == GPIO.HIGH

    def sensor_volgende_plank_active(self):
        """Controleer of sensor 1 actief is (hoog signaal)"""
        return GPIO.input(self.sensor_volgende_plank) == GPIO.HIGH

    def sensor_home_active(self):
        """Controleer of sensor 1 actief is (hoog signaal)"""
        return GPIO.input(self.sensor_home) == GPIO.HIGH

    def sensor_einde_active(self):
        """Controleer of sensor 1 actief is (hoog signaal)"""
        return GPIO.input(self.sensor_einde) == GPIO.HIGH


    def cleanup(self):
        self._motor_pwm.stop()
        GPIO.output(self.DIR_PIN, GPIO.LOW) # Zet de DIR-pin veilig op LOW
        self.all_off()
        GPIO.cleanup()
        print("GPIO cleanup uitgevoerd.")

    def __del__(self):
        self.cleanup()
        print("RelayController object is verwijderd.")
        
"""if __name__ == "__main__":
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
        del controller  # Roept __del__ aan → cleanup """

    
