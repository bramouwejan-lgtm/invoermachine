import time
from RelayController import RelayController

def test_mock_functionaliteit():
    print("--- Start Test met MockGPIO ---")
    
    # 1. Initialisatie
    print("\n1. Initialiseren van controller...")
    # We hoeven geen motor_pwm mee te geven, de mock maakt intern een dummy PWM aan
    controller = RelayController()
    
    # 2. Test Relais
    print("\n2. Testen van Relais (Relay 0 AAN zetten)...")
    # Let op: In de code is LOW = AAN, HIGH = UIT
    controller.set_relay(0, True) # True -> LOW (AAN)
    time.sleep(0.5)
    
    print("   Testen van Relais (Relay 0 UIT zetten)...")
    controller.set_relay(0, False) # False -> HIGH (UIT)
    
    # 3. Test Stappenmotor
    print("\n3. Testen van Stappenmotor (Start CW)...")
    controller.start_stappenmotor('CW', 500) # 500 steps/sec
    time.sleep(1)
    
    print("   Snelheid verhogen...")
    controller.start_stappenmotor('CW', 1000)
    time.sleep(0.5)
    
    print("   Stoppen...")
    controller.stop_stappenmotor()
    
    # 4. Test Sensoren (Simulatie)
    # We kunnen de interne state van de MockGPIO manipuleren om een sensor te simuleren
    print("\n4. Testen van Sensoren...")
    # Dit werkt alleen als we toegang hebben tot de onderliggende GPIO klasse, 
    # maar via de controller lezen we gewoon de waarde.
    # Standaard geeft de mock LOW terug als er niets is ingesteld.
    
    is_active = controller.sensor_plank_active()
    print(f"   Sensor plank actief? {is_active} (Verwacht: False/Low in mock default)")
    
    print("\n--- Einde Test ---")
    # Bij het afsluiten wordt __del__ aangeroepen -> cleanup

if __name__ == "__main__":
    test_mock_functionaliteit()

