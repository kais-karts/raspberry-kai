import api
import threading
import time
from serial_comms import driver

item_names = [
  "Banana",
  "Bomb",
  "redShroom",
  "goldShroom",
  "redShell",
  "blueShell",
  "lightning",
  "bulletBill",
]

if __name__ == "__main__":
    # threading.Thread(target=driver).start()  # Run main() in a different thread
    driver()
