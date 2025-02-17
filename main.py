from app import get_app, get_socket
import api
import threading
import time

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

def main():
    while True:
        for j in range(8):
            for i in range(10):
                time.sleep(1)
                print(f"{i}s")
            print(item_names[j])
            api.item_pickup(j)

if __name__ == "__main__":
    threading.Thread(target=main).start()  # Run main() in a different thread
    flask()  # Run flask() in the main thread
