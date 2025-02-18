# Serial Port Settings
SERIAL_PORT = '/dev/ttyACM0'  # or '/dev/serial0' on a Raspberry Pi
BAUD_RATE = 115200

# Define constants
NUM_ANCHORS = 2   # for AnchorDistances
NUM_KARTS = 6     # for RankingUpdate

ITEM_DURATION = [3, 10, 5, 6, 15, 10, 5, 7] # (in seconds)

ITEMS = ['Banana', 'Bomb', 'redShroom', 'lightning', 'bulletBill', 'gold_shroom', 'red_shell', 'blue_shell']

BUFF_ITEMS = {'redShroom', 'goldShroom','bulletBill'}
DEBUFF_ITEMS = {'Banana', 'Bomb', 'redShell', 'blueShell', 'lightning'}

ITEM_SPEED = [0, 0, 2, 1, 2, 2, 0, 0]

# Define the magic number (packet start marker)
PACKET_START_MAGIC = 0xDEADBEEF
PACKET_LEN_BYTES = 24

# Define your GPIO pin numbers (adjust to your wiring)
NORMAL_PIN = 13
SLOW_PIN = 5
STOP_PIN = 6

KART_ID = 0

BUTTON_IN, BUTTON_OUT= 27, 22

