import RPi.GPIO as GPIO

# Define your GPIO pin numbers (adjust to your wiring)
NORMAL_PIN = 5
SLOW_PIN = 6
STOP_PIN = 13

# Setup GPIO - Initialized at full speed
GPIO.setmode(GPIO.BCM)
GPIO.setup(NORMAL_PIN, GPIO.OUT)
GPIO.setup(SLOW_PIN, GPIO.OUT)
GPIO.setup(STOP_PIN, GPIO.OUT)
GPIO.output(NORMAL_PIN, GPIO.LOW)
GPIO.output(SLOW_PIN, GPIO.LOW)
GPIO.output(STOP_PIN, GPIO.LOW)

def full_speed():
    # Equivalent to: digitalWrite(SLOW_PIN, LOW); digitalWrite(NORMAL_PIN, LOW); digitalWrite(D2, LOW);
    GPIO.output(SLOW_PIN, GPIO.LOW)
    GPIO.output(NORMAL_PIN, GPIO.LOW)
    GPIO.output(STOP_PIN, GPIO.LOW)

def normal_speed():
    # Equivalent to: digitalWrite(SLOW_PIN, LOW); digitalWrite(NORMAL_PIN, HIGH); digitalWrite(D2, LOW);
    GPIO.output(SLOW_PIN, GPIO.LOW)
    GPIO.output(NORMAL_PIN, GPIO.HIGH)
    GPIO.output(STOP_PIN, GPIO.LOW)

def slow_speed():
    # Equivalent to: digitalWrite(NORMAL_PIN, LOW); digitalWrite(SLOW_PIN, HIGH); digitalWrite(D2, LOW);
    GPIO.output(NORMAL_PIN, GPIO.LOW)
    GPIO.output(SLOW_PIN, GPIO.HIGH)
    GPIO.output(STOP_PIN, GPIO.LOW)

def no_speed():
    GPIO.output(NORMAL_PIN, GPIO.LOW)
    GPIO.output(SLOW_PIN, GPIO.LOW)
    GPIO.output(STOP_PIN, GPIO.HIGH)
