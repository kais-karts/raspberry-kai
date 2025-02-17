from app import get_app, get_socket
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

app = get_app()
socketio = get_socket()

ui_connected_event = threading.Event()


def flask():
    socketio.run(app, port=8000, debug=True, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=driver).start()  # Run main() in a different thread
    flask()  # Run flask() in the main thread
