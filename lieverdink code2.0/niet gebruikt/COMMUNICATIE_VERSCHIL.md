# Belangrijk: Twee Verschillende Communicatie Format

Er zijn nu **twee verschillende JSON formaten** voor communicatie met motors:

## 1. Stappenmotorcontroler.py (Huidige Implementatie)
```json
{
  "message": "s",      // Kleine letter
  "Breedte": 1000,
  "Forward": "T",      // "T" voor vooruit
  "Speed": 1500
}
```

Dit gebruikt:
- Kleine letters voor keys
- "T" of "F" als strings voor forward
- "Speed" parameter

**Bedoeld voor**: Directe motor controller via RX/TX

## 2. Serial_controler.py (Meadow Implementatie)
```json
{
  "Message": "Start",  // Grote letters + volledige woorden
  "Breedte": 1000,
  "Forward": true      // true/false boolean
}
```

Dit gebruikt:
- Grote letters voor keys (Message, Breedte, Forward)
- Boolean values voor forward
- "Start", "Stop", "Update", "Error" als berichten

**Bedoeld voor**: Meadow Motor Controller

## Wanneer Welke Gebruiken?

### Gebruik `serial_controler.py` als:
- Je communiceert met de Meadow
- Je gebruikt het oude C# systeem
- Je JSON formaat moet zijn: `{"Message": "Start", "Forward": true}`

### Gebruik `stappenmotorcontroler.py` als:
- Je direct met een motor controller board communiceert
- Je een nieuw formaat gebruikt: `{"message": "s", "Forward": "T"}`
- Je snelheid wilt instellen via `Speed` parameter

## Converteren Tussen Formats

Als je één module wilt voor beide, kun je een adapter maken:

```python
def convert_to_meadow_format(message_type, breedte, forward):
    """Converteer naar Meadow formaat"""
    message = {
        "Message": "Start" if message_type == "s" else "Stop",
        "Breedte": breedte,
        "Forward": True if forward == "T" else False
    }
    return json.dumps(message)

def convert_to_new_format(message, breedte, forward):
    """Converteer naar nieuw formaat"""
    message_type = "s" if message == "Start" else "T"
    forward_str = "T" if forward else "F"
    data = {
        "message": message_type,
        "Breedte": breedte,
        "Forward": forward_str
    }
    return json.dumps(data)
```

## Aanbeveling

Voor consistentie, kies één formaat en gebruik die overal:

### Optie A: Gebruik Meadow Formaat (Aanbevolen voor C# integratie)
```json
{
  "Message": "Start",
  "Breedte": 1000,
  "Forward": true
}
```

### Optie B: Gebruik Nieuw Formaat
```json
{
  "message": "s",
  "Breedte": 1000,
  "Forward": "T",
  "Speed": 1500
}
```

## Quick Reference

| Actie | Meadow (serial_controler.py) | Nieuw (stappenmotorcontroler.py) |
|-------|------------------------------|----------------------------------|
| Forward | `{"Message": "Start", "Breedte": 1000, "Forward": true}` | `{"message": "s", "Breedte": 1000, "Forward": "T", "Speed": 1500}` |
| Backward | `{"Message": "Start", "Breedte": 1000, "Forward": false}` | `{"message": "s", "Breedte": 1000, "Forward": "F", "Speed": 1500}` |
| Stop | `{"Message": "Stop"}` | `{"message": "T", "Breedte": 0, "Forward": "F"}` |
| Home | `{"Message": "Start"}` | Zelfde als backward |

## Voor Code Herschrijven

Als je de oude Meadow code integreert, gebruik dan `serial_controler.py`.

Als je een nieuwe implementatie maakt, gebruik dan `stappenmotorcontroler.py` met de nieuwere features.

