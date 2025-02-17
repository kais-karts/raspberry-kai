import typing
from typing import NamedTuple, List, Literal

class Position(NamedTuple):
    name: str
    x: int
    y: int


def update_positions(positions: List[Position]) -> None:
    """
    Updates positions of players on map takes in ordered list of racers with x,y positons 1st place in 0th index 2nd place in 1st etc...
    """
    pass


def item_pickup(item: int) -> None:
    """
    Updates the UI when a new item is picked up
    """
    socketio.emit('item_pickup', {'item': item})


def item_hit(item: int) -> None:
    """
    Updates UI when player is hit with item
    """
    socketio.emit('item_hit', {'item': item})

def item_use(duration: float) -> None:
    """
    Updates UI when player uses an item
    """
    socketio.emit('item_use', {'duration': duration})





