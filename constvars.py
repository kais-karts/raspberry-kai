# Serial Port Settings
SERIAL_PORT = '/dev/ttyUSB0'  # or '/dev/serial0' on a Raspberry Pi
BAUD_RATE = 115200

# Define constants
NUM_ANCHORS = 2   # for AnchorDistances
NUM_KARTS = 6     # for RankingUpdate

ITEM_DURATION = 5 # (in seconds)


# import numpy as np

# # Configure Mariokart item weights 1st, 2nd, 3rd, 4th, 5th, 6th
# # https://www.mariowiki.com/Mario_Kart_8_item_probability_distributions
# Banana = [30, 20, 20, 0, 0, 0]
# Bomb = [0, 0, 10, 15, 15, 0]
# redShroom = [30, 25, 50, 30, 10, 0]
# goldShroom = [0, 0, 0, 10, 50, 50]
# redShell = [0, 30, 30, 20, 10, 0]
# blueShell = [0, 0, 10, 20, 10, 0]
# lightning = [0, 0, 0, 5, 10, 10]
# bulletBill = [0,0,0,0,0,50]

# # combine all items and normalize
# all_items = np.array([Banana, Bomb, redShroom, goldShroom, redShell, blueShell, lightning, bulletBill])
# all_items = all_items / all_items.sum(axis=0)

ITEMS = ['Banana', 'Bomb', 'redShroom', 'goldShroom', 'redShell', 'blueShell', 'lightning', 'bulletBill']

# def draw_item(place):
#     """Draw an item based on the place."""
#     return np.random.choice(item_names, p=all_items[:, place-1])


# # Test the function by generating 10 items for each place
# for place in range(1, 7):
#     items = [draw_item(place) for _ in range(10)]
#     print(f"Place {place}: {items}")