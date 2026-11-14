# Wiring and pin connections

| Module | Signal | Arduino Uno |
|---|---|---:|
| SG90 servo | Signal | D9 |
| SG90 servo | VCC | Regulated 5 V supply |
| SG90 servo | GND | Common GND |
| Active buzzer | + / - | D8 / GND |
| Red LED | Anode via 220–330 ohm resistor | D6 |
| Green LED | Anode via 220–330 ohm resistor | D7 |
| Both LEDs | Cathode | GND |
| Manual open button | Terminals | D2 and GND |
| Manual close button | Terminals | D3 and GND |
| I²C LCD | SDA / SCL | A4 / A5 |
| I²C LCD | VCC / GND | 5 V / GND |

Buttons use INPUT_PULLUP, so each switch connects its input pin to GND when pressed.

## Power and safety
- Prefer a separate regulated 5 V supply for the servo, sized for its current demand. Join its ground to Arduino GND.
- Do not draw servo stall current from the Uno 5 V pin.
- The sketch assumes LCD I²C address 0x27; some modules use 0x3F.
- Use current-limiting resistors for LEDs. Use a transistor driver if the buzzer load exceeds safe GPIO current.
- Webcams connect to the computer over USB, not to Uno pins.
- Verify polarity and module ratings before powering the circuit.
