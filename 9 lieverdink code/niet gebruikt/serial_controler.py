"""
Serial Controller voor Raspberry Pi
Verstuur JSON commando's naar de Meadow via seriële communicatie

Het formaat dat de Meadow verwacht:
{
  "Message": "Start",  # Of "Stop", "Update", "Error"
  "Breedte": 1000,     # Aantal stappen
  "Forward": true       # true voor vooruit, false voor achteruit
}
"""

import serial
import json
import time


class SerialController:
    def __init__(self, port='/dev/ttyS0', baudrate=115200):
        """
        Initialiseer de serial controller.
        
        Args:
            port: Seriële poort (standaard: /dev/ttyS0 voor GPIO UART)
            baudrate: Baudrate (standaard: 115200)
        """
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        print(f"SerialController wordt geïnitialiseerd...")
    
    def connect(self):
        """Maak verbinding met de seriële poort."""
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Verbonden met {self.port} op {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"Fout bij verbinden met {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Sluit de seriële verbinding."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Seriële verbinding gesloten")
    
    def send_message(self, message, breedte=None, forward=None):
        """
        Verstuur een bericht naar de Meadow.
        
        Args:
            message: "Start", "Stop", "Update", of "Error"
            breedte: Aantal stappen (optioneel, alleen bij "Start")
            forward: True voor vooruit, False voor achteruit (optioneel, alleen bij "Start")
        
        Returns:
            bool: True als succesvol, False anders
        """
        if not self.connection or not self.connection.is_open:
            print("Niet verbonden! Gebruik connect() eerst.")
            return False
        
        # Maak het JSON object
        data = {
            "Message": message
        }
        
        # Voeg Breedte toe als opgegeven
        if breedte is not None:
            data["Breedte"] = breedte
        
        # Voeg Forward toe als opgegeven
        if forward is not None:
            data["Forward"] = forward
        
        # Converteer naar JSON string
        json_string = json.dumps(data)
        
        print(f"Verstuur: {json_string}")
        
        try:
            # Verstuur het bericht met een newline erachter
            self.connection.write((json_string + '\n').encode('utf-8'))
            print("Bericht succesvol verstuurd!")
            return True
        except Exception as e:
            print(f"Fout bij versturen: {e}")
            return False
    
    def motor_start_forward(self, breedte):
        """
        Start de motor naar voren.
        
        Args:
            breedte: Aantal stappen
        """
        return self.send_message("Start", breedte=breedte, forward=True)
    
    def motor_start_backward(self, breedte):
        """
        Start de motor naar achteren.
        
        Args:
            breedte: Aantal stappen
        """
        return self.send_message("Start", breedte=breedte, forward=False)
    
    def motor_return_home(self):
        """
        Stuur motor terug naar home positie.
        """
        return self.send_message("Start")  # Geen breedte en forward = return home
    
    def motor_stop(self):
        """
        Stop de motor.
        """
        return self.send_message("Stop")
    
    def motor_update(self):
        """
        Vraag update/calibratie informatie.
        """
        return self.send_message("Update")
    
    def cleanup(self):
        """Sluit de verbinding."""
        self.disconnect()


# Test functie
if __name__ == "__main__":
    # Maak een controller instantie
    # Pas de poort aan naar jouw setup
    controller = SerialController(port='/dev/ttyS0', baudrate=115200)
    
    try:
        # Verbind met de Meadow
        if not controller.connect():
            print("Kon geen verbinding maken!")
            exit(1)
        
        print("\n=== Test Serial Communicatie ===\n")
        
        # Test 1: Motor naar voren (voorwaarts)
        print("Test 1: Motor start naar voren (2000 stappen)")
        controller.motor_start_forward(breedte=2000)
        time.sleep(2)
        
        # Test 2: Motor naar achteren
        print("\nTest 2: Motor start naar achteren (1000 stappen)")
        controller.motor_start_backward(breedte=1000)
        time.sleep(2)
        
        # Test 3: Motor stop
        print("\nTest 3: Motor stoppen")
        controller.motor_stop()
        time.sleep(1)
        
        # Test 4: Motor return home
        print("\nTest 4: Motor terug naar home")
        controller.motor_return_home()
        time.sleep(2)
        
        # Test 5: Vraag update
        print("\nTest 5: Vraag update/calibratie")
        controller.motor_update()
        
        print("\n=== Test voltooid ===")
        
    except KeyboardInterrupt:
        print("\nAfsluiten...")
    except Exception as e:
        print(f"Fout: {e}")
    finally:
        controller.cleanup()

