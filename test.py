import threading
# import keyboard
from pynput import keyboard
import api
from app import get_app, get_socket

app = get_app()
socketio = get_socket()
item = 0

def flask():
    # Run Flask (via SocketIO) in the main thread
    socketio.run(app, port=8000, debug=True, use_reloader=False)

def on_press(key):
    global item
    try:
        char = key.char
        if char.isdigit():
            item = int(char)
            if item >= 8:
                item = 7
    except AttributeError:
        if key == keyboard.Key.enter:
            print("Item Pickup")
            api.item_pickup(item)
        elif key == keyboard.Key.space:
            print("Item Hit")
            api.item_hit(item)
        elif key == keyboard.Key.shift:
            print("Item Use")
            api.item_use(item)
        else:
            print(f"Unrecognized trigger key: {key}")

def main():
    """
    The main function will set up the keyboard listener in a separate thread
    so that we can still run the Flask app in the main thread.
    """
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # Run the keyboard listener in a background thread
    threading.Thread(target=main, daemon=True).start()
    flask()
    # main()
