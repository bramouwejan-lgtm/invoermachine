# Stappenmotor Controller - Verbinding Handleiding

## Nieuwe Verbindingsfuncties

De `StepperMotorController` heeft nu uitgebreide verbindingsfuncties:

### 1. `is_connected()`
Controleer of de motor controller verbonden is.
```python
if controller.is_connected():
    print("Verbonden!")
```

### 2. `test_connection()`
Test de verbinding door een test commando te versturen.
```python
if controller.test_connection():
    print("Verbinding werkt!")
else:
    print("Verbinding gefaald")
```

### 3. `reconnect()`
Herstel de verbinding als deze verbroken is.
```python
if not controller.is_connected():
    controller.reconnect()
```

### 4. `list_available_ports()`
Lijst alle beschikbare seriële poorten.
```python
ports = StepperMotorController.list_available_ports()
# Output:
# Beschikbare seriële poorten:
#   - COM3: USB Serial Port
#   - COM4: Arduino Uno
```

## Basis Gebruik

```python
from RelayController import RelayController
from stappenmotorcontroler import StepperMotorController

# 1. Zoek beschikbare poorten
ports = StepperMotorController.list_available_ports()

# 2. Maak een RelayController
relay_controller = RelayController()

# 3. Maak de motor controller met de juiste poort
controller = StepperMotorController(
    relay_controller=relay_controller,
    port=ports[0],  # Gebruik eerste beschikbare poort
    baudrate=9600
)

# 4. Test de verbinding
if controller.test_connection():
    print("Motor controller is verbonden!")
    
    # 5. Gebruik de motor
    controller.motor_forward(breedte=2000)  # Stopt bij sensor_einde
    controller.motor_backward(breedte=1000)  # Stopt bij sensor_home
    controller.motor_home()  # Gaat naar home en stopt bij sensor_home
```

## Problemen Oplossen

### Verbinding werkt niet?
```python
# Controleer beschikbare poorten
StepperMotorController.list_available_ports()

# Probeer handmatig te verbinden
controller.reconnect()

# Test de verbinding
controller.test_connection()
```

### Verkeerde poort?
```python
# Kies een specifieke poort
controller = StepperMotorController(
    relay_controller=relay_controller,
    port='COM3',  # Of '/dev/ttyUSB0' op Linux
    baudrate=9600
)
```

