"""

bbare minimum pi -> esp example

"""
from logging import getLogger
import serial
from constvars import *
from pi_read import read_packet
from speed_control import *
import threading
import time
from .api import (item_pickup, item_hit, update_positions, item_use)
import liveTriJson as tri

logger = getLogger("SerialReader")

def init():
    try:
        global ser
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logger.info(f"Opened serial port {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        logger.error(f"Failed to open serial port {SERIAL_PORT}: {e}")
        exit() # No point continuing if we can't open serial

def delayed_call(duration: int):
    if (duration):
        time.sleep(duration)
    else:
        time.sleep(ITEM_DURATION)
    normal_speed()

# ITEMS = ['Banana', 'Bomb', 'redShroom', 'goldShroom', 'redShell', 'blueShell', 'lightning', 'bulletBill']


    # 3 = UseItem, 4 = RankingUpdate, 5 = GetItem, 6 = DoItem

def driver():
    init()
    tri.init()
    while True:
        read_packet()
        if 'tag' in CURRENT_PACKET:
            match CURRENT_PACKET['tag']:
                case 3:
                    item_use(CURRENT_PACKET['args'])
                case 4:
                    update_positions
                case 5:
                    item_pickup
                case 6:
                    item_hit
                case 'hit':
                    item_hit(CURRENT_PACKET['args']['item'])
                case 'use':
                    use_item(CURRENT_PACKET['args']['item'])
        print("Dumping Variables:\nGlobals:\n%s, %s\nConstants:\n%s, %s", CURRENT_PACKET, ser, SERIAL_PORT, BAUD_RATE, NUM_ANCHORS, NUM_KARTS)
        if 'tag' in CURRENT_PACKET and 'item' in CURRENT_PACKET:

            # match CURRENT_PACKET['item']:
            #     case 0:
            #         # Banana
            #         no_speed()
            #         t = threading.Thread(target=delayed_call, args=(3))
            #         t.start()
            #     case 1:
            #         # Bomb
            #         no_speed()
            #         t = threading.Thread(target=delayed_call, args=(10))
            #         t.start()
            #     case 2:
            #         # redShroom
            #         full_speed()
            #         t = threading.Thread(target=delayed_call, args=(3))
            #         t.start()
            #     case 3:
            #         # goldShroom
            #         full_speed()
            #         t = threading.Thread(target=delayed_call ,args=(10))
            #         t.start()
            #     case 4:
            #         # redShell
            #         no_speed()
            #         t = threading.Thread(target=delayed_call, args=(5))
            #         t.start()
            #     case 5:
            #         # blueShell
            #         no_speed()
            #         t = threading.Thread(target=delayed_call, args=(5))
            #         t.start()
            #     case 6:
            #         # lightning
            #         slow_speed()
            #         t = threading.Thread(target=delayed_call)
            #         t.start()
            #     case 7:
            #         # bulletBill
            #         no_speed()
            #         t = threading.Thread(target=delayed_call, args=(20))
            #         t.start()

    