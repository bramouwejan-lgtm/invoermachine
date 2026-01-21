# Seriële Signaal Guide - Raspberry Pi naar Meadow

## Overzicht

De Raspberry Pi communiceert met de Meadow via seriële communicatie (RX/TX poorten).
Het signaal bevat JSON objecten in het volgende formaat.

## JSON Formaat

### Algemeen formaat:
```json
{
  "Message": "Start",     // Of "Stop", "Update", "Error"
  "Breedte": 1000,        // Aantal stappen (optioneel)
  "Forward": true         // true/false voor richting (optioneel)
}
```

## Beschikbare Commando's

### 1. Motor Start - Vooruit
```json
{
  "Message": "Start",
  "Breedte": 2000,
  "Forward": true
}
```

### 2. Motor Start - Achteruit
```json
{
  "Message": "Start",
  "Breedte": 1000,
  "Forward": false
}
```

### 3. Motor Stop
```json
{
  "Message": "Stop"
}
```

### 4. Motor Return Home
```json
{
  "Message": "Start"
}
```
(Let op: geen Breedte en Forward = return home)

### 5. Vraag Update/Calibratie
```json
{
  "Message": "Update"
}
```

## Python Implementaties

### Optie 1: Volledige SerialController Klasse

```python
from serial_controler import SerialController

# Initialiseer
controller = SerialController(port='/dev/ttyS0', baudrate=115200)

# Verbind
controller.connect()

# Gebruik de functies
controller.motor_start_forward(2000)    # 2000 stappen vooruit
controller.motor_start_backward(1000)  # 1000 stappen achteruit
controller.motor_return_home()         # Terug naar home
controller.motor_stop()                # Stop motor
controller.motor_update()              # Vraag calibratie

# Sluit verbinding
controller.cleanup()
```

### Optie 2: Simpele Functies

```python
import serial
from simple_serial import *

# Open verbinding
conn = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# Gebruik functies
motor_forward(conn, 2000)     # Vooruit
motor_backward(conn, 1000)   # Achteruit
motor_stop(conn)              # Stop
motor_home(conn)              # Home

# Sluit verbinding
conn.close()
```

### Optie 3: Handmatig JSON Versturen

```python
import serial
import json

# Open verbinding
conn = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# Maak JSON object
command = {
    "Message": "Start",
    "Breedte": 1500,
    "Forward": True
}

# Verstuur
json_string = json.dumps(command)
conn.write((json_string + '\n').encode('utf-8'))

# Sluit verbinding
conn.close()
```

## Seriële Poorten

Op de Raspberry Pi:
- `/dev/ttyS0` - Hardware UART (GPIO 14/15)
- `/dev/ttyUSB0` - USB naar Serial adapter

Op de Meadow:
- COM1 → `/dev/ttyS0` op Raspberry Pi
- COM4 → `/dev/ttyS1` op Raspberry Pi

## Baudrate

Standaard baudrate: **115200**

## Voorbeeld Integratie

```python
from RelayController import RelayController
from serial_controler import SerialController
import time

# Maak controllers
relay = RelayController()
motor = SerialController(port='/dev/ttyS0', baudrate=115200)

# Verbind
motor.connect()

try:
    # Controleer sensors
    if not relay.sensor_einde_active():
        # Motor vooruit
        motor.motor_start_forward(2000)
        
        # Wacht en controleer
        while True:
            if relay.sensor_einde_active():
                motor.motor_stop()
                break
            time.sleep(0.1)
    
finally:
    motor.cleanup()
```

## Fout Afhandeling

```python
from serial_controler import SerialController

motor = SerialController()
motor.connect()

# Probeer commando
if motor.motor_start_forward(1000):
    print("Success!")
else:
    print("Fout bij versturen!")

# Herstel bij fout
if not motor.connection.is_open:
    print("Verbinding verbroken, probeer opnieuw...")
    motor.connect()

motor.cleanup()
```

## Voorbeelden

### Sensor-Based Motor Control
```python
from RelayController import RelayController
from serial_controler import SerialController

relay = RelayController()
motor = SerialController()

if motor.connect():
    # Ga vooruit tot sensor_einde
    if not relay.sensor_einde_active():
        motor.motor_start_forward(5000)  # Groot getal, sensor stopt het
        
        # Monitor sensor
        import time
        while not relay.sensor_einde_active():
            time.sleep(0.1)
        
        motor.motor_stop()
```

### Precisie Beweging
```python
# Small movements voor precisie
motor.motor_start_forward(100)
motor.motor_start_backward(50)
motor.motor_stop()
```

### Return to Home Sequence
```python
# Return to home
motor.motor_return_home()

# Wacht even
time.sleep(3)

# Check of we op home zijn
if relay.sensor_home_active():
    print("Motor is op home positie")
```

