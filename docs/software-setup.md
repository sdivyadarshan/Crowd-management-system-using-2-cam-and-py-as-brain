# Software setup

## Python
Recommended: Python 3.10 in a virtual environment.

Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The first run may download yolov8n.pt. Keep the weights in the working directory or update MODEL_PATH.

## Arduino IDE
1. Install Arduino IDE 2.x.
2. Install Arduino AVR Boards through Boards Manager if needed.
3. Select Arduino Uno and the correct COM port.
4. Install a LiquidCrystal_I2C library compatible with lcd.init().
5. Wire and Servo are included with the standard Arduino environment.
6. Upload src/arduino/parking_gate_controller.ino.

## Configuration
The Python defaults are entry camera index 1, exit camera index 2, Arduino COM8, and 9600 baud. These are computer-specific; edit the constants at the top of the Python script if needed. Close Serial Monitor before running Python.

## Run

```bash
python src/python/dual_camera_parking.py
```

Enter a positive parking capacity. Press R in a camera window to reset or Esc to exit.
