"""
Simpele functies voor seriële communicatie met Meadow Motor Controller

Gebruik:
    from simple_serial import send_command
    
    # Open verbinding
    serial_conn = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    
    # Stuur commando
    send_command(serial_conn, 'Start', breedte=2000, forward=True)
"""

import serial
import json


def send_command(connection, message, breedte=None, forward=None):
    """
    Stuur een commando naar de Meadow via seriële verbinding.
    
    Args:
        connection: Seriële verbinding object
        message: "Start", "Stop", "Update", of "Error"
        breedte: Aantal stappen (optioneel)
        forward: True voor vooruit, False voor achteruit (optioneel)
    
    Returns:
        bool: True als succesvol
    """
    # Maak JSON object
    data = {"Message": message}
    
    if breedte is not None:
        data["Breedte"] = breedte
    
    if forward is not None:
        data["Forward"] = forward
    
    # Converteer naar JSON en verstuur
    json_string = json.dumps(data)
    print(f"Verstuur: {json_string}")
    
    try:
        connection.write((json_string + '\n').encode('utf-8'))
        return True
    except Exception as e:
        print(f"Fout: {e}")
        return False


def motor_forward(connection, steps):
    """Stuur motor vooruit."""
    return send_command(connection, "Start", breedte=steps, forward=True)


def motor_backward(connection, steps):
    """Stuur motor achteruit."""
    return send_command(connection, "Start", breedte=steps, forward=False)


def motor_home(connection):
    """Stuur motor naar home positie."""
    return send_command(connection, "Start")


def motor_stop(connection):
    """Stop de motor."""
    return send_command(connection, "Stop")


# Standalone test
if __name__ == "__main__":
    # Verbind met seriële poort
    conn = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    
    print("Seriële communicatie test")
    
    # Motor vooruit
    motor_forward(conn, 1000)
    
    # Motor achteruit
    motor_backward(conn, 500)
    
    # Motor stop
    motor_stop(conn)
    
    # Motor home
    motor_home(conn)
    
    # Sluit verbinding
    conn.close()

