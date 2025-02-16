import numpy as np
from flask import Flask, request, render_template
from flask_socketio import SocketIO 
from flask_socketio import emit 
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler


app = Flask(__name__)
socketio = SocketIO(app)

def get_app(): return app
def get_socket(): return socketio

class Kart:
    def __init__(self, id, name, current_item, location):
        self.id = id
        self.name = name
        self.current_item = current_item
        self.location = location

    def get_name(self):
        # Remove the dash and capitalize the name
        return self.name.replace("-", " ").title()

    def __str__(self):
        return f"{self.name, self.location, self.current_item}"


def scale_location(location, map_width, map_height):
    x, y = location
    return (x / map_width * 100, y / map_height * 100)


# Register the custom filter
@app.template_filter("scale_location")
def scale_location_filter(location):
    map_width = 300
    map_height = 400
    return scale_location(location, map_width, map_height)


karts = []


@app.route("/")
@app.route("/index")
def index():
    karts = [
        Kart(1, "mario", "Banana", (150, 150)),
        Kart(2, "luigi", "Green Shell", (200, 115)),
        Kart(3, "Toad", "Mushroom", (32, 240)),
        Kart(4, "bowser", "Fireball", (91, 67)),
        Kart(5, "donkey-kong", "Barrel", (190, 230)),
        Kart(6, "waluigi", "Bob-omb", (150, 320)),
    ]
    return render_template("index.html", karts=karts)


def get_ranking():
    """Rerank the karts based on their position"""
    pass


def use_item(kart: Kart):
    """Upon request from a kart, use their active item"""

    kart.current_item = None


def get_item():
    """
    Get a random item from the item list
    Triggered when kart passes a checkpoint
    """
    pass


def get_message():
    """
    Called when a kart sends a message to the server
    """
    message = ""
    id = 0
    new_position = (0, 0)
    if message == "update":
        update_position(id, new_position)
    elif message == "ability":
        use_item()


def update_position(id, new_position):
    # Get kart by id from karts list
    kart = [kart for kart in karts if kart.id == id][0]
    kart.location = new_position

# Websockets



# @app.route("/")
# def index():
#     return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print("Client connected!")
    socketio.emit("server_message", {"message": "Hello from Flask-SocketO!"})

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected!")


# if __name__ == "__main__":
#     socketio.run(app, port=8000, debug=True)