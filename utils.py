import numpy as np
import constvars

# Configure Mariokart item weights 1st, 2nd, 3rd, 4th, 5th, 6th
# https://www.mariowiki.com/Mario_Kart_8_item_probability_distributions
Banana = [30, 20, 20, 0, 0, 0]
Bomb = [0, 0, 10, 15, 15, 0]
redShroom = [30, 25, 50, 30, 10, 0]
goldShroom = [0, 0, 0, 10, 50, 50]
redShell = [0, 30, 30, 20, 10, 0]
blueShell = [0, 0, 10, 20, 10, 0]
lightning = [0, 0, 0, 5, 10, 10]
bulletBill = [0,0,0,0,0,50]

# combine all items and normalize
all_items = np.array([Banana, Bomb, redShroom, lightning, bulletBill, goldShroom, redShell, blueShell])
all_items = all_items / all_items.sum(axis=0)

def draw_item(place):
    """Draw an item based on the place."""
    choice = constvars.ITEMS.index(np.random.choice(constvars.ITEMS, p=all_items[:, place-1]))
    print(f"Random choice yieled {choice} from {all_items[:, place-1]} given place {place}")
    return choice