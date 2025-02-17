# Serial Port Settings
SERIAL_PORT = '/dev/ttyUSB0'  # or '/dev/serial0' on a Raspberry Pi
BAUD_RATE = 115200

# Define constants
NUM_ANCHORS = 2   # for AnchorDistances
NUM_KARTS = 6     # for RankingUpdate

ITEM_DURATION = [3, 10, 3, 10, 5, 5, 5, 20] # (in seconds)

ITEMS = ['Banana', 'Bomb', 'redShroom', 'goldShroom', 'redShell', 'blueShell', 'lightning', 'bulletBill']

ITEM_SPEED = [0, 0, 2, 2, 0, 0, 1, 0]
