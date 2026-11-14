#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo gateServo;

const byte SERVO_PIN = 9;
const byte BUZZER_PIN = 8;
const byte RED_LED_PIN = 6;
const byte GREEN_LED_PIN = 7;
const byte MANUAL_OPEN_PIN = 2;
const byte MANUAL_CLOSE_PIN = 3;

const int CLOSED_ANGLE = 0;
const int OPEN_ANGLE = 90;
const unsigned long DEBOUNCE_MS = 250;
const unsigned long BEEP_ON_MS = 180;
const unsigned long BEEP_GAP_MS = 180;

int availableSlots = 0;
String serialBuffer = "";
unsigned long lastOpenPress = 0;
unsigned long lastClosePress = 0;
unsigned long buzzerChangedAt = 0;
byte completedBeeps = 0;
bool warningActive = false;
bool buzzerOn = false;

void updateDisplay() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("PARKING SYSTEM");
  lcd.setCursor(0, 1);
  if (availableSlots <= 0) {
    lcd.print("NO SLOTS");
  } else {
    lcd.print("Available: ");
    lcd.print(availableSlots);
  }
}

void setGate(bool open) {
  if (open && availableSlots <= 0) open = false;
  gateServo.write(open ? OPEN_ANGLE : CLOSED_ANGLE);
  digitalWrite(GREEN_LED_PIN, open ? HIGH : LOW);
  digitalWrite(RED_LED_PIN, open ? LOW : HIGH);
}

void startTwoBeeps() {
  warningActive = true;
  buzzerOn = false;
  completedBeeps = 0;
  buzzerChangedAt = 0;
}

void serviceBuzzer() {
  if (!warningActive) {
    digitalWrite(BUZZER_PIN, LOW);
    return;
  }
  unsigned long now = millis();
  unsigned long interval = buzzerOn ? BEEP_ON_MS : BEEP_GAP_MS;
  if (buzzerChangedAt == 0 || now - buzzerChangedAt >= interval) {
    if (buzzerOn) {
      digitalWrite(BUZZER_PIN, LOW);
      buzzerOn = false;
      completedBeeps++;
      if (completedBeeps >= 2) warningActive = false;
    } else {
      digitalWrite(BUZZER_PIN, HIGH);
      buzzerOn = true;
    }
    buzzerChangedAt = now;
  }
}

void processCommand(String command) {
  command.trim();
  if (command == "O") {
    setGate(true);
  } else if (command == "C") {
    setGate(false);
  } else if (command == "E") {
    startTwoBeeps();
  } else if (command.startsWith("S")) {
    availableSlots = command.substring(1).toInt();
    if (availableSlots < 0) availableSlots = 0;
    if (availableSlots == 0) setGate(false);
    updateDisplay();
  }
}

void readSerial() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n') {
      processCommand(serialBuffer);
      serialBuffer = "";
    } else if (c != '\r' && serialBuffer.length() < 24) {
      serialBuffer += c;
    } else if (serialBuffer.length() >= 24) {
      serialBuffer = "";
    }
  }
}

void checkButtons() {
  unsigned long now = millis();
  if (digitalRead(MANUAL_OPEN_PIN) == LOW &&
      now - lastOpenPress >= DEBOUNCE_MS) {
    lastOpenPress = now;
    if (availableSlots > 0) setGate(true);
    else {
      setGate(false);
      startTwoBeeps();
    }
  }
  if (digitalRead(MANUAL_CLOSE_PIN) == LOW &&
      now - lastClosePress >= DEBOUNCE_MS) {
    lastClosePress = now;
    setGate(false);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(MANUAL_OPEN_PIN, INPUT_PULLUP);
  pinMode(MANUAL_CLOSE_PIN, INPUT_PULLUP);
  digitalWrite(BUZZER_PIN, LOW);

  gateServo.attach(SERVO_PIN);
  lcd.init();
  lcd.backlight();

  // Safe power-up state: gate closed.
  setGate(false);
  lcd.setCursor(0, 0);
  lcd.print("SYSTEM READY");
  lcd.setCursor(0, 1);
  lcd.print("Waiting for PC");
}

void loop() {
  readSerial();
  checkButtons();
  serviceBuzzer();
}
