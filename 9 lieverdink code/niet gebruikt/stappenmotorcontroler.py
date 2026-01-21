import serial
import json
import time

class StepperMotorController:
    def __init__(self, relay_controller, port='/dev/ttyUSB0', baudrate=9600, default_speed=1000):
        """
        Initialiseer de stappenmotor controller.
        
        Args:
            relay_controller: RelayController instantie voor sensor checks
            port: Het seriële poort adres (standaard: /dev/ttyUSB0)
            baudrate: Baudrate voor seriële communicatie (standaard: 9600)
            default_speed: Standaard snelheid (RPM of stappen per seconde, standaard: 1000)
        """
        self.relay_controller = relay_controller
        self.port = port
        self.baudrate = baudrate
        self.default_speed = default_speed
        self.serial_connection = None
        print(f"StepperMotorController wordt geïnitialiseerd met standaard snelheid: {default_speed}")
        
    def _connect(self):
        """Maak verbinding met de seriële poort."""
        try:
            if self.serial_connection is None or not self.serial_connection.is_open:
                self.serial_connection = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=1
                )
                print(f"Verbonden met {self.port} op {self.baudrate} baud")
        except serial.SerialException as e:
            print(f"Fout bij verbinden met {self.port}: {e}")
            raise
    
    def is_connected(self):
        """
        Controleer of de verbinding actief is.
        
        Returns:
            bool: True als verbonden, False anders
        """
        try:
            return self.serial_connection is not None and self.serial_connection.is_open
        except:
            return False
    
    def test_connection(self):
        """
        Test de verbinding door een ping commando te versturen.
        
        Returns:
            bool: True als verbinding werkt, False anders
        """
        try:
            if not self.is_connected():
                print("Niet verbonden. Maak verbinding...")
                self._connect()
            
            # Test verbinding door een klein test commando te versturen
            test_command = {"message": "T", "Breedte": 0, "Forward": "F"}
            command_json = json.dumps(test_command)
            self.serial_connection.write((command_json + '\n').encode('utf-8'))
            print("Verbindingstest succesvol!")
            return True
        except Exception as e:
            print(f"Verbindingstest gefaald: {e}")
            return False
    
    def reconnect(self):
        """
        Herstellen van de seriële verbinding.
        """
        try:
            print("Poging tot herverbinden...")
            if self.serial_connection and self.serial_connection.is_open:
                self._disconnect()
            self._connect()
            print("Herverbonden!")
            return True
        except Exception as e:
            print(f"Herverbinden gefaald: {e}")
            return False
    
    @staticmethod
    def list_available_ports():
        """
        Lijst alle beschikbare seriële poorten op.
        
        Returns:
            list: Lijst met beschikbare poorten
        """
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        available_ports = []
        
        print("Beschikbare seriële poorten:")
        for port in ports:
            print(f"  - {port.device}: {port.description}")
            available_ports.append(port.device)
        
        return available_ports
    
    def _send_command(self, message_type, breedte, forward, speed=None):
        """
        Verstuur een commando naar de motor controller.
        
        Args:
            message_type: "s" (start), "T" (stop), of "U" (update)
            breedte: De afstand/stappen voor de beweging
            forward: "T" voor vooruit, "F" voor achteruit
            speed: De snelheid (RPM of stappen per seconde). None gebruikt default_speed
        """
        self._connect()
        
        # Gebruik default snelheid als geen snelheid is opgegeven
        if speed is None:
            speed = self.default_speed
        
        command = {
            "message": message_type,
            "Breedte": breedte,
            "Forward": forward,
            "Speed": speed  # Voeg snelheid toe aan commando
        }
        
        # Converteer naar JSON string
        command_json = json.dumps(command)
        
        print(f"Verstuur commando: {command_json}")
        
        # Verstuur het commando
        self.serial_connection.write((command_json + '\n').encode('utf-8'))
    
    def _disconnect(self):
        """Sluit de seriële verbinding."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Seriële verbinding gesloten")
    
    def _monitor_forward(self, max_time=30):
        """
        Monitor de motor tijdens voorwaartse beweging.
        Stopt als sensor_einde actief wordt of na max_time seconden.
        
        Args:
            max_time: Maximale tijd in seconden om te monitoren (standaard: 30)
        """
        start_time = time.time()
        while (time.time() - start_time) < max_time:
            # Controleer of sensor_einde actief is geworden
            if self.relay_controller.sensor_einde_active():
                print("Sensor_einde gedetecteerd! Motor stoppen...")
                self.motor_stop()
                return
            
            time.sleep(0.1)
        
        print(f"Monitor timeout bereikt na {max_time} seconden")
    
    def motor_forward(self, breedte=1000, speed=None, monitor=True):
        """
        Beweeg de stappenmotor naar voren.
        Stopt automatisch als sensor_einde actief wordt.
        
        Args:
            breedte: De afstand/stappen voor de beweging (standaard: 1000)
            speed: De snelheid (RPM of stappen per seconde). None gebruikt default_speed
            monitor: Of de sensor moet worden gemonitord (standaard: True)
        """
        # Controleer of sensor_einde al actief is
        if self.relay_controller.sensor_einde_active():
            print("ERROR: De stappenmotor is al aan het einde, kan niet verder naar voren!")
            return
        
        print(f"Stappenmotor gaat naar voren met breedte: {breedte}, snelheid: {speed if speed else self.default_speed}")
        try:
            # Start de beweging
            self._send_command("s", breedte, "T", speed=speed)
            
            if monitor:
                # Schat de benodigde tijd gebaseerd op snelheid
                current_speed = speed if speed else self.default_speed
                estimated_time = (breedte / current_speed) * 2  # 2x buffer voor veiligheid
                # Voeg wat buffer tijd toe en monitor
                max_time = max(estimated_time, 5)  # Minimaal 5 seconden
                self._monitor_forward(max_time=max_time)
                
        except Exception as e:
            print(f"Fout bij motor naar voren: {e}")
            self.motor_stop()
    
    def _monitor_backward(self, max_time=30):
        """
        Monitor de motor tijdens achterwaartse beweging.
        Stopt als sensor_home actief wordt of na max_time seconden.
        
        Args:
            max_time: Maximale tijd in seconden om te monitoren (standaard: 30)
        """
        start_time = time.time()
        while (time.time() - start_time) < max_time:
            # Controleer of sensor_home actief is geworden
            if self.relay_controller.sensor_home_active():
                print("Sensor_home gedetecteerd! Motor stoppen...")
                self.motor_stop()
                return
            
            time.sleep(0.1)
        
        print(f"Monitor timeout bereikt na {max_time} seconden")
    
    def motor_backward(self, breedte=1000, speed=None, monitor=True):
        """
        Beweeg de stappenmotor naar achteren.
        Stopt automatisch als sensor_home actief wordt.
        
        Args:
            breedte: De afstand/stappen voor de beweging (standaard: 1000)
            speed: De snelheid (RPM of stappen per seconde). None gebruikt default_speed
            monitor: Of de sensor moet worden gemonitord (standaard: True)
        """
        # Controleer of sensor_home al actief is
        if self.relay_controller.sensor_home_active():
            print("ERROR: De stappenmotor is al op home positie, kan niet verder naar achteren!")
            return
        
        print(f"Stappenmotor gaat naar achteren met breedte: {breedte}, snelheid: {speed if speed else self.default_speed}")
        try:
            # Start de beweging
            self._send_command("s", breedte, "F", speed=speed)
            
            if monitor:
                # Schat de benodigde tijd gebaseerd op snelheid
                current_speed = speed if speed else self.default_speed
                estimated_time = (breedte / current_speed) * 2  # 2x buffer voor veiligheid
                # Voeg wat buffer tijd toe en monitor
                max_time = max(estimated_time, 5)  # Minimaal 5 seconden
                self._monitor_backward(max_time=max_time)
                
        except Exception as e:
            print(f"Fout bij motor naar achteren: {e}")
            self.motor_stop()
    
    def motor_home(self, max_steps=5000, speed=None):
        """
        Home de stappenmotor (gaat terug naar beginpositie).
        Gebruikt de motor_backward functie die automatisch stopt bij sensor_home.
        
        Args:
            max_steps: Maximum aantal stappen om te bewegen tijdens homen (standaard: 5000)
            speed: De snelheid (RPM of stappen per seconde). None gebruikt default_speed
        """
        print(f"Stappenmotor gaat naar home positie met max {max_steps} stappen, snelheid: {speed if speed else self.default_speed}")
        # Gebruik motor_backward die automatisch stopt bij sensor_home
        self.motor_backward(breedte=max_steps, speed=speed)
    
    def motor_stop(self):
        """
        Stop de stappenmotor.
        """
        print("Stappenmotor stoppen")
        try:
            self._send_command("T", 0, "F")
        except Exception as e:
            print(f"Fout bij motor stoppen: {e}")
    
    def motor_update(self, breedte, forward, speed=None):
        """
        Update de stappenmotor met nieuwe parameters.
        
        Args:
            breedte: De afstand/stappen voor de beweging
            forward: "T" voor vooruit, "F" voor achteruit
            speed: De snelheid (RPM of stappen per seconde). None gebruikt default_speed
        """
        print(f"Update stappenmotor: breedte={breedte}, forward={forward}, snelheid: {speed if speed else self.default_speed}")
        try:
            self._send_command("U", breedte, forward, speed=speed)
        except Exception as e:
            print(f"Fout bij motor update: {e}")
    
    def set_speed(self, speed):
        """
        Wijzig de standaard snelheid van de motor controller.
        
        Args:
            speed: De nieuwe standaard snelheid (RPM of stappen per seconde)
        """
        self.default_speed = speed
        print(f"Standaard snelheid aangepast naar: {speed}")
    
    def cleanup(self):
        """Sluit de seriële verbinding."""
        self._disconnect()
        print("StepperMotorController cleanup uitgevoerd.")
    
    def __del__(self):
        """Cleanup bij verwijdering van het object."""
        self.cleanup()
        print("StepperMotorController object is verwijderd.")


# Test functies
if __name__ == "__main__":
    # Importeer RelayController
    from RelayController import RelayController
    
    # Laat beschikbare poorten zien
    print("\n=== Beschikbare seriële poorten ===")
    available_ports = StepperMotorController.list_available_ports()
    
    if not available_ports:
        print("Geen seriële poorten gevonden!")
        exit(1)
    
    # Maak eerst een RelayController instantie
    relay_controller = RelayController()
    
    # Maak een instantie van de controller met de RelayController
    # Pas de port aan naar jouw seriële poort (bijvoorbeeld: '/dev/ttyUSB0' of 'COM3' op Windows)
    # Je kunt ook de eerste beschikbare poort gebruiken
    port = available_ports[0] if available_ports else '/dev/ttyUSB0'
    print(f"\nGebruik poort: {port}")
    
    # Maak controller met standaard snelheid
    controller = StepperMotorController(relay_controller=relay_controller, port=port, baudrate=9600, default_speed=1500)
    
    try:
        print("\n=== Test Stappenmotor Controller ===\n")
        
        # Test verbinding
        print("Test: Verbinding testen...")
        if controller.test_connection():
            print("✓ Verbinding is OK")
        else:
            print("✗ Verbinding gefaald")
            
        # Controleer verbindingsstatus
        if controller.is_connected():
            print("✓ Motor controller is verbonden")
        else:
            print("✗ Motor controller is niet verbonden")
        
        # Test: Motor naar voren met verschillende snelheden
        print("\nTest 1: Motor naar voren (standaard snelheid)")
        controller.motor_forward(breedte=2000)
        
        print("\nTest 2: Motor naar voren (langzame snelheid: 500)")
        controller.motor_forward(breedte=2000, speed=500)
        
        print("\nTest 3: Motor naar voren (snelle snelheid: 2500)")
        controller.motor_forward(breedte=2000, speed=2500)
        
        # Test: Motor naar achteren met verschillende snelheden
        print("\nTest 4: Motor naar achteren (standaard snelheid)")
        controller.motor_backward(breedte=1000)
        
        print("\nTest 5: Motor naar achteren (traag: 800)")
        controller.motor_backward(breedte=1000, speed=800)
        
        # Test: Motor homen (stopt automatisch bij sensor_home)
        print("\nTest 6: Motor homen (traag voor precisie)")
        controller.motor_home(max_steps=5000, speed=1000)
        
        # Test: Verander standaard snelheid
        print("\nTest 7: Verander standaard snelheid naar 2000")
        controller.set_speed(2000)
        controller.motor_forward(breedte=1500)  # Gebruikt nu 2000 als snelheid
        
        print("\n=== Test voltooid ===")
        
    except KeyboardInterrupt:
        print("Afsluiten...")
    except Exception as e:
        print(f"Fout opgetreden: {e}")
    finally:
        del controller
        del relay_controller
