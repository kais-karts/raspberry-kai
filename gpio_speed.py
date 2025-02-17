import RPi.GPIO as GPIO
from typing import Optional
from constvars import NORMAL_PIN, SLOW_PIN, STOP_PIN

# Setup GPIO - Initialized at full speed
GPIO.setmode(GPIO.BCM)
GPIO.setup(NORMAL_PIN, GPIO.OUT)
GPIO.setup(SLOW_PIN, GPIO.OUT)
GPIO.setup(STOP_PIN, GPIO.OUT)
GPIO.output(NORMAL_PIN, GPIO.LOW)
GPIO.output(SLOW_PIN, GPIO.HIGH)
GPIO.output(STOP_PIN, GPIO.LOW)

# Setup GPIO - Initialized at full speed
GPIO.setmode(GPIO.BCM)
GPIO.setup(NORMAL_PIN, GPIO.OUT)
GPIO.setup(SLOW_PIN, GPIO.OUT)
GPIO.setup(STOP_PIN, GPIO.OUT)
GPIO.output(NORMAL_PIN, GPIO.LOW)
GPIO.output(SLOW_PIN, GPIO.HIGH)
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

def set_speed(speed: Optional[int]):
    if speed == 0:
        no_speed()
    elif speed == 1:
        slow_speed()
    elif speed == 2:
        full_speed()
    else:
        normal_speed()