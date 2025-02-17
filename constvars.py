# Serial Port Settings
SERIAL_PORT = '/dev/ttyACM0'  # or '/dev/serial0' on a Raspberry Pi
BAUD_RATE = 115200

# Define constants
NUM_ANCHORS = 2   # for AnchorDistances
NUM_KARTS = 6     # for RankingUpdate

ITEM_DURATION = [3, 10, 3, 10, 5, 5, 5, 20] # (in seconds)

ITEMS = ['Banana', 'Bomb', 'redShroom', 'goldShroom', 'redShell', 'blueShell', 'lightning', 'bulletBill']

ITEM_SPEED = [0, 0, 2, 2, 0, 0, 1, 0]

# Define the magic number (packet start marker)
PACKET_START_MAGIC = 0xDEADBEEF
PACKET_LEN_BYTES = 24

# Define your GPIO pin numbers (adjust to your wiring)
NORMAL_PIN = 5
SLOW_PIN = 6
STOP_PIN = 13

KART_ID = 0

BUTTON_IN, BUTTON_OUT= 17, 27

