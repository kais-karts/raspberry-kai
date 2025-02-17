from logging import getLogger
import serial
import constvars
from pi_read import read_packet
from speed_control import *
import liveTriJson as tri
import globals

logger = getLogger("SerialReader")

def init():
    try:
        globals.ser = serial.Serial(constvars.SERIAL_PORT, constvars.BAUD_RATE, timeout=1)
        logger.info(f"Opened serial port {constvars.SERIAL_PORT} at {constvars.BAUD_RATE} baud.")
    except Exception as e:
        logger.error(f"Failed to open serial port {constvars.SERIAL_PORT}: {e}")
        exit() # No point continuing if we can't open serial

def driver():
    init()
    tri.init()
    while True:
        data = read_packet()
        # TODO: time.sleep(0.1) to prevent busy loop?