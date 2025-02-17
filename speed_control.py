import time
import gpio_speed
import threading
import constvars

def delayed_call(duration: int):
    time.sleep(duration)
    gpio_speed.normal_speed()

def speed_control(item: int):
    gpio_speed.set_speed(constvars.ITEM_SPEED[item])
    t = threading.Thread(target=delayed_call, args=(constvars.ITEM_DURATION[item],))
    t.start()
