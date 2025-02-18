from logging import getLogger
import serial
import constvars
from pi_read import read_packet, init_send, tests, use_item
import liveTriJson as tri
import globals
import gpio_logic as io
import time
import RPi.GPIO as GPIO
import ui_comms as ui
import asyncio
import threading

logger = getLogger("SerialReader")

def init():
    try:
        globals.ser = serial.Serial(constvars.SERIAL_PORT, constvars.BAUD_RATE, timeout=1)
        logger.info(f"Opened serial port {constvars.SERIAL_PORT} at {constvars.BAUD_RATE} baud.")
    except Exception as e:
        logger.error(f"Failed to open serial port {constvars.SERIAL_PORT}: {e}")
        exit() # No point continuing if we can't open serial
    init_send()

def driver():
    init()
    tri.init()
    io.setup()
    t = threading.Thread(target=ui.init)
    t.start()
    # attach event listener to GPIO pin
    GPIO.add_event_detect(constvars.BUTTON_IN, GPIO.RISING, callback=use_item)
    print("System initialized.")
    while True:
        data = read_packet()
        time.sleep(0.01)
