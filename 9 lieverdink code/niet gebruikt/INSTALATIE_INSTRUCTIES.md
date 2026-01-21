# Installatie Instructies voor Raspberry Pi

## Vereiste Python Packages Installeren

### Op de Raspberry Pi

```bash
# Installeer pyserial
sudo pip3 install pyserial

# Of als je pip gebruikt zonder sudo
pip3 install --user pyserial

# Controleer of het is geïnstalleerd
python3 -c "import serial; print('pyserial is geïnstalleerd!')"
```

### Installeer alle dependencies

```bash
# Ga naar het project directory
cd "/path/to/lieverdink code2.0"

# Installeer alle requirements (als je een requirements.txt hebt)
pip3 install -r requirements.txt

# Of installeer handmatig:
pip3 install pyserial
pip3 install RPi.GPIO
```

## Test of Alles Werkt

### 1. Test seriële verbinding

```python
import serial
print("Serial library werkt!")
```

### 2. Test GPIO (RelayController)

```python
import RPi.GPIO as GPIO
print("RPi.GPIO werkt!")
```

### 3. Test de controllers

```bash
# Test comhandeler
python3 comhandeler.py

# Test stappenmotor controller
python3 stappenmotorcontroler_nieuw.py
```

## Mogelijke Problemen

### Probleem: "Permission denied" bij seriële poort

**Oplossing:**
```bash
# Voeg gebruiker toe aan dialout groep
sudo usermod -a -G dialout $USER

# Herstart (of log opnieuw in)
sudo reboot
```

### Probleem: "ModuleNotFoundError: No module named 'serial'"

**Oplossing:**
```bash
# Installeer pyserial
sudo pip3 install pyserial

# Of gebruik pip
pip3 install --user pyserial
```

### Probleem: "Permission denied" bij GPIO

**Oplossing:**
```bash
# Voeg gebruiker toe aan gpio groep
sudo usermod -a -G gpio $USER

# Herstart
sudo reboot
```

## Seriële Poort Vinden

### Lijst van beschikbare poorten:

```bash
# Linux command
ls /dev/tty*

# Of specifiek voor Raspberry Pi
ls /dev/ttyS*    # Hardware UART
ls /dev/ttyUSB*  # USB to Serial
```

### Python script om poorten te vinden:

```python
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Poort: {port.device} - {port.description}")
```

## Automatische Installatie Script

Maak een `install.sh` bestand:

```bash
#!/bin/bash
# install.sh

echo "Installeer dependencies..."

# Installeer pyserial
sudo pip3 install pyserial

# Installeer RPi.GPIO
sudo pip3 install RPi.GPIO

# Voeg gebruiker toe aan groepen
sudo usermod -a -G dialout $USER
sudo usermod -a -G gpio $USER

echo "Installatie voltooid!"
echo "Herstart de Raspberry Pi of log opnieuw in."
```

Gebruik:
```bash
chmod +x install.sh
./install.sh
```

## Verifiëring Checklist

Na installatie, controleer:

- [ ] `import serial` werkt zonder errors
- [ ] `import RPi.GPIO as GPIO` werkt zonder errors  
- [ ] Seriële poort is beschikbaar (`/dev/ttyS0` of `/dev/ttyUSB0`)
- [ ] GPIO pins zijn niet geïnitialiseerd door andere programma's
- [ ] Sensor pinnen zijn correct verbonden (GPIO 9 en 10)

## Snelle Test

Run dit om te testen:

```python
#!/usr/bin/env python3
# test_install.py

print("Test dependencies...")

try:
    import serial
    print("✓ serial library geïnstalleerd")
except ImportError:
    print("✗ serial library NIET gevonden")
    print("  Run: pip3 install pyserial")

try:
    import RPi.GPIO as GPIO
    print("✓ RPi.GPIO library geïnstalleerd")
except ImportError:
    print("✗ RPi.GPIO library NIET gevonden")
    print("  Run: pip3 install RPi.GPIO")

try:
    from RelayController import RelayController
    print("✓ RelayController.py kan worden geïmporteerd")
except ImportError as e:
    print(f"✗ RelayController.py kan niet worden geïmporteerd: {e}")

try:
    from comhandeler import motor_forward
    print("✓ comhandeler.py kan worden geïmporteerd")
except ImportError as e:
    print(f"✗ comhandeler.py kan niet worden geïmporteerd: {e}")

print("\nTest voltooid!")
```

## Troubleshooting

### Als alles faalt:

```bash
# Update package lists
sudo apt-get update

# Install Python en pip
sudo apt-get install python3 python3-pip

# Installeer packages
sudo pip3 install pyserial RPi.GPIO

# Controleer versies
python3 --version
pip3 --version
```

### Als je SSH gebruikt:

Zorg ervoor dat SSH toegang heeft:
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

