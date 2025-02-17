import time
import gpio_speed
import threading
import globals

def delayed_call(duration: int):
    time.sleep(duration)
    gpio_speed.normal_speed()

def speed_control(item: int):
    gpio_speed.set_speed(globals.ITEM_SPEED[item])
    t = threading.Thread(target=delayed_call, args=(globals.ITEM_DURATION[item],))
    t.start()
