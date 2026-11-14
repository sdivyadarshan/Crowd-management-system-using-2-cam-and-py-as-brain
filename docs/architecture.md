# System architecture

## Computer / Python layer
- OpenCV captures two independent USB webcam streams.
- YOLO detects people; separate ByteTrack states track each camera.
- The centroid of each tracked person is tested against a vertical crossing line.
- Entry and exit events update estimated occupancy.
- Python calculates available capacity and sends serial commands.

## Arduino / embedded layer
- Receives newline-terminated commands at 9600 baud.
- Drives servo gate and red/green status LEDs.
- Updates the 16×2 I²C LCD.
- Generates two beeps for a full-capacity entry attempt.
- Reads manual open and close buttons.

## Data flow

```text
Entry webcam ─┐
              ├─> OpenCV ─> YOLO person detection ─> ByteTrack
Exit webcam ──┘                                      |
                                                     v
                                  Centroid history + line crossing
                                                     |
                                                     v
                                Occupancy / available-slot calculation
                                                     |
                                            USB serial, 9600 baud
                                                     |
                                                     v
                   Arduino Uno ─> Servo / LCD / LEDs / buzzer
                               └─> Manual push buttons
```

## Protocol

| Message | Meaning |
|---|---|
| S<number> | Set available slots |
| O | Open gate if capacity is available |
| C | Close gate |
| E | Play two warning beeps |

Occupancy starts at zero on program launch and is not persisted between runs.
