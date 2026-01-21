#!/usr/bin/env python3
"""
Test script om te controleren of alle dependencies geïnstalleerd zijn.
Run dit op de Raspberry Pi om te zien wat er mist.
"""

print("=== Dependency Checker ===\n")

# Test 1: serial library
print("1. Test serial library...")
try:
    import serial
    print("   ✓ serial library OK")
    try:
        import serial.tools.list_ports
        print("   ✓ serial.tools.list_ports OK")
    except ImportError:
        print("   ✗ serial.tools.list_ports MISSING")
        print("      Dit zou mee moeten komen met pyserial")
except ImportError:
    print("   ✗ serial library NIET GEVONDEN")
    print("      Installeer met: sudo pip3 install pyserial")

# Test 2: RPi.GPIO library
print("\n2. Test RPi.GPIO library...")
try:
    import RPi.GPIO as GPIO
    print("   ✓ RPi.GPIO OK")
except ImportError:
    print("   ✗ RPi.GPIO NIET GEVONDEN")
    print("      Installeer met: sudo pip3 install RPi.GPIO")
except RuntimeError as e:
    print(f"   ! RPi.GPIO RUNTIME ERROR: {e}")
    print("      Dit is normaal als je niet op een Raspberry Pi draait")

# Test 3: Comhandeler
print("\n3. Test comhandeler.py...")
try:
    from comhandeler import send_command, motor_forward, motor_backward, motor_stop, motor_home
    print("   ✓ comhandeler.py OK")
except ImportError as e:
    print(f"   ✗ comhandeler.py NIET GEVONDEN: {e}")
    print("      Zorg dat comhandeler.py in dezelfde directory staat")

# Test 4: RelayController
print("\n4. Test RelayController.py...")
try:
    from RelayController import RelayController
    print("   ✓ RelayController.py OK")
except ImportError as e:
    print(f"   ✗ RelayController.py NIET GEVONDEN: {e}")
    print("      Zorg dat RelayController.py in dezelfde directory staat")
except Exception as e:
    print(f"   ! RelayController ERROR: {e}")
    print("      Dit kan normaal zijn buiten Raspberry Pi")

# Test 5: StappenmotorController
print("\n5. Test stappenmotorcontroler_nieuw.py...")
try:
    from stappenmotorcontroler_nieuw import StappenmotorControllerNieuw
    print("   ✓ stappenmotorcontroler_nieuw.py OK")
except ImportError as e:
    print(f"   ✗ stappenmotorcontroler_nieuw.py ERROR: {e}")

# Test 6: Seriële poorten (alleen op Raspberry Pi)
print("\n6. Test seriële poorten...")
try:
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    if ports:
        print("   Beschikbare poorten:")
        for port in ports:
            print(f"     - {port.device}: {port.description}")
    else:
        print("   ! Geen seriële poorten gevonden")
        print("      Dit is normaal buiten Raspberry Pi")
except Exception as e:
    print(f"   ! Kan poorten niet lezen: {e}")

print("\n=== Check Voltooid ===")
print("\nAls er errors zijn, zie INSTALATIE_INSTRUCTIES.md voor oplossingen")

