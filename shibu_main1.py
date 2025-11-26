#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ===================== MOTOR PINS =====================
int EN1 = 2, IN1 = 22, IN2 = 23;
int EN2 = 3, IN3 = 24, IN4 = 25;
int EN3 = 4, IN5 = 26, IN6 = 27;
int EN4 = 5, IN7 = 28, IN8 = 29;

// ===================== EYE GEOMETRY =====================
struct Eye {
  int x, y, r;
  int pupilX, pupilY;
};

Eye leftEye  = {40, 32, 12, 0, 0};
Eye rightEye = {88, 32, 12, 0, 0};

String currentMode = "NEUTRAL";

// ===================== RANDOM EYE MOTION =====================
unsigned long lastMove = 0;
const unsigned long moveInterval = 5000;

// ===================== AUTO-STOP (5 SECONDS) =====================
unsigned long actionStart = 0;
bool actionRunning = false;

// ===================== EYE DRAW HELPERS =====================
void drawEye(const Eye &eye, bool closed = false) {
  if (closed) {
    display.drawLine(eye.x - eye.r, eye.y, eye.x + eye.r, eye.y, SH110X_WHITE);
  } else {
    display.drawCircle(eye.x, eye.y, eye.r, SH110X_WHITE);
    display.fillCircle(eye.x + eye.pupilX, eye.y + eye.pupilY, 4, SH110X_WHITE);
  }
}

void drawDualEyes(bool closed = false) {
  display.clearDisplay();
  drawEye(leftEye, closed);
  drawEye(rightEye, closed);
  display.display();
}

// ===================== EMOTIONS =====================
void setEmotion(const String &emo) {
  String e = emo; e.toUpperCase();
  currentMode = e;

  leftEye.y = rightEye.y = 32;
  leftEye.pupilX = rightEye.pupilX = 0;
  leftEye.pupilY = rightEye.pupilY = 0;
  leftEye.r = rightEye.r = 12;

  if (e == "HAPPY") {
    leftEye.y = rightEye.y = 30;
    leftEye.pupilY = rightEye.pupilY = 2;
  } else if (e == "SAD") {
    leftEye.y = rightEye.y = 36;
    leftEye.pupilY = rightEye.pupilY = -2;
  } else if (e == "ANGRY") {
    leftEye.y = 30; rightEye.y = 34;
  } else if (e == "SURPRISED") {
    leftEye.r = rightEye.r = 15;
  } else if (e == "LEFT") {
    leftEye.pupilX = rightEye.pupilX = -3;
  } else if (e == "RIGHT") {
    leftEye.pupilX = rightEye.pupilX = 3;
  } else if (e == "UP") {
    leftEye.pupilY = rightEye.pupilY = -3;
  } else if (e == "DOWN") {
    leftEye.pupilY = rightEye.pupilY = 3;
  } else if (e == "WINK") {
    display.clearDisplay();
    drawEye(leftEye, false);
    drawEye(rightEye, true);
    display.display();
    return;
  } else if (e == "BLINK") {
    drawDualEyes(true);
    delay(200);
    drawDualEyes(false);
    return;
  }

  drawDualEyes(false);
}

// ===================== RANDOM EYE MOTION =====================
void randomEyeMotion() {
  unsigned long now = millis();
  if (now - lastMove > moveInterval && currentMode == "NEUTRAL") {
    leftEye.pupilX  = random(-3, 4);
    rightEye.pupilX = random(-3, 4);
    leftEye.pupilY  = random(-2, 3);
    rightEye.pupilY = random(-2, 3);
    drawDualEyes(false);
    lastMove = now;
  }
}

// ===================== MOTOR FUNCTIONS =====================
void enableMotors() {
  analogWrite(EN1, 200);
  analogWrite(EN2, 200);
  analogWrite(EN3, 200);
  analogWrite(EN4, 200);
}

void stopAll() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW); digitalWrite(IN6, LOW);
  digitalWrite(IN7, LOW); digitalWrite(IN8, LOW);
  analogWrite(EN1, 0); analogWrite(EN2, 0);
  analogWrite(EN3, 0); analogWrite(EN4, 0);
}

void forward() {
  enableMotors();
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  digitalWrite(IN5, HIGH); digitalWrite(IN6, LOW);
  digitalWrite(IN7, HIGH); digitalWrite(IN8, LOW);
}

void backward() {
  enableMotors();
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  digitalWrite(IN5, LOW); digitalWrite(IN6, HIGH);
  digitalWrite(IN7, LOW); digitalWrite(IN8, HIGH);
}

void leftTurn() {
  enableMotors();
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  digitalWrite(IN5, HIGH); digitalWrite(IN6, LOW);
  digitalWrite(IN7, HIGH); digitalWrite(IN8, LOW);
}

void rightTurn() {
  enableMotors();
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW); digitalWrite(IN6, HIGH);
  digitalWrite(IN7, LOW); digitalWrite(IN8, HIGH);
}

// ===================== SETUP =====================
void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(IN5, OUTPUT); pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT); pinMode(IN8, OUTPUT);

  pinMode(EN1, OUTPUT); pinMode(EN2, OUTPUT);
  pinMode(EN3, OUTPUT); pinMode(EN4, OUTPUT);

  stopAll();

  if (!display.begin(0x3C, true)) {
    Serial.println("❌ OLED FAILED");
    while (1);
  }

  randomSeed(analogRead(0));
  setEmotion("NEUTRAL");
}

void loop() {
  randomEyeMotion();

  // ---- AUTO STOP AFTER 5 SECONDS ----
  if (actionRunning && (millis() - actionStart >= 5000)) {
    stopAll();
    setEmotion("NEUTRAL");
    actionRunning = false;
  }

  // ---- READ SERIAL COMMANDS ----
  if (Serial.available()) {

    // Stop any previous action immediately
    stopAll();
    actionRunning = false;

    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // NEW command starts fresh timer
    actionRunning = true;
    actionStart = millis();

    if (cmd == "F") { forward(); setEmotion("UP"); }
    else if (cmd == "B") { backward(); setEmotion("DOWN"); }
    else if (cmd == "L") { leftTurn(); setEmotion("LEFT"); }
    else if (cmd == "R") { rightTurn(); setEmotion("RIGHT"); }
    else if (cmd == "S") {
      stopAll();
      setEmotion("NEUTRAL");
      actionRunning = false;
    }
  }
}