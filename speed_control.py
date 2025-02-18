import time
import gpio_logic
import threading
import globals
import constvars

def delayed_call(item: int, duration: int):
    if globals.affect_lock.acquire(blocking=False):
        print("<Item Applied>")
        gpio_logic.set_speed(constvars.ITEM_SPEED[item])
        time.sleep(duration)
        print("!Speed Restored!")
        gpio_logic.normal_speed()
        globals.affect_lock.release()
    else:
        print("Affect lock already held, item not applied.")

def speed_control(item: int):
    t = threading.Thread(target=delayed_call, args=(item, constvars.ITEM_DURATION[item],))
    t.start()
