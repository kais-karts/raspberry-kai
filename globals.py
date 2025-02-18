import threading

global ser
global TRACK_LIST, TRACK_SET, BEACONS, UPDATE_TIME, last_point, start_time
global seen_uids
global rankings
global kart_item
global kart_rank
global x
global y
global counter
global affect_lock #prevents multiple hits

ser = None
seen_uids = set()
rankings = []
kart_item = None
kart_rank = None
counter = None
affect_lock = threading.Lock()
x = 0
y = 0

def update_position(new_x, new_y):
    global x, y
    x = new_x
    y = new_y
    return

def get_position():
    global x, y
    return x, y

