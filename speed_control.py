import time
import gpio_speed
import threading
import globals

def delayed_call(duration: int):
    time.sleep(duration)
    gpio_speed.normal_speed()

def speed_control(item: int):
    match item:
        case 0:
            # Banana
            gpio_speed.no_speed()
        case 1:
            # Bomb
            gpio_speed.no_speed()
        case 2:
            # redShroom
            gpio_speed.full_speed()
        case 3:
            # goldShroom
            gpio_speed.full_speed()
        case 4:
            # redShell
            gpio_speed.no_speed()
        case 5:
            # blueShell
            gpio_speed.no_speed()
        case 6:
            # lightning
            gpio_speed.slow_speed()
        case 7:
            # bulletBill
            gpio_speed.no_speed()
    t = threading.Thread(target=delayed_call, args=(globals.ITEM_DURATION[item],))
    t.start()
