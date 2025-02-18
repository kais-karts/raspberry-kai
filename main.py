import threading
import time
from serial_comms import driver

if __name__ == "__main__":
    # threading.Thread(target=driver).start()  # Run main() in a different thread
    driver()
