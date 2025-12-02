import sys

class MockGPIO:
    """
    Een mock klasse om RPi.GPIO te simuleren op niet-Raspberry Pi systemen (zoals Windows).
    """
    BCM = "BCM"
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0
    PUD_UP = "PUD_UP"
    PUD_DOWN = "PUD_DOWN"
    FALLING = "FALLING"
    RISING = "RISING"
    BOTH = "BOTH"

    _pin_states = {}
    _pin_modes = {}
    _callbacks = {}

    @staticmethod
    def setmode(mode):
        print(f"[MOCK GPIO] Mode ingesteld op: {mode}")

    @staticmethod
    def setup(pin, mode, pull_up_down=None):
        pud_str = f", pull_up_down={pull_up_down}" if pull_up_down else ""
        print(f"[MOCK GPIO] Setup pin {pin} als {mode}{pud_str}")
        MockGPIO._pin_modes[pin] = mode
        # Standaard status voor inputs
        if mode == MockGPIO.IN:
             MockGPIO._pin_states[pin] = MockGPIO.LOW # Of HIGH afhankelijk van PUD, maar LOW is veilige aanname

    @staticmethod
    def output(pin, state):
        state_str = "HIGH" if state == MockGPIO.HIGH else "LOW"
        print(f"[MOCK GPIO] Output pin {pin} -> {state_str}")
        MockGPIO._pin_states[pin] = state

    @staticmethod
    def input(pin):
        # Geeft de laatst bekende status terug, of LOW als onbekend
        val = MockGPIO._pin_states.get(pin, MockGPIO.LOW)
        # print(f"[MOCK GPIO] Read pin {pin} -> {val}") # Commentaar weg voor veel debug info
        return val

    @staticmethod
    def cleanup():
        print("[MOCK GPIO] Cleanup uitgevoerd")
        MockGPIO._pin_states = {}
        MockGPIO._pin_modes = {}

    @staticmethod
    def setwarnings(flag):
        print(f"[MOCK GPIO] Warnings ingesteld op: {flag}")

    @staticmethod
    def add_event_detect(pin, edge, callback=None, bouncetime=None):
        print(f"[MOCK GPIO] Event detect toegevoegd op pin {pin}, edge={edge}, bouncetime={bouncetime}")
        if callback:
            MockGPIO._callbacks[pin] = callback

    class PWM:
        def __init__(self, pin, freq):
            print(f"[MOCK GPIO] PWM aangemaakt op pin {pin} met frequentie {freq}Hz")
            self.pin = pin
            self.freq = freq
            self.duty_cycle = 0

        def start(self, duty_cycle):
            self.duty_cycle = duty_cycle
            print(f"[MOCK GPIO] PWM start op pin {self.pin} met duty cycle {duty_cycle}%")

        def ChangeDutyCycle(self, duty_cycle):
            self.duty_cycle = duty_cycle
            print(f"[MOCK GPIO] PWM pin {self.pin} duty cycle gewijzigd naar {duty_cycle}%")

        def ChangeFrequency(self, freq):
            self.freq = freq
            print(f"[MOCK GPIO] PWM pin {self.pin} frequentie gewijzigd naar {freq}Hz")

        def stop(self):
            print(f"[MOCK GPIO] PWM stop op pin {self.pin}")

# Vervang de echte RPi.GPIO module door deze mock als we niet op een Pi zitten
if 'RPi' not in sys.modules:
    import types
    rpi_module = types.ModuleType('RPi')
    rpi_module.GPIO = MockGPIO
    sys.modules['RPi'] = rpi_module
    sys.modules['RPi.GPIO'] = MockGPIO

