```
ssh raspberrypi@192.168.1.124
```

username: raspberrypi
OR
username: kai
password: kart

open in browser

```
chromium http://127.0.0.1:8000
```

```
free -h
```

# Using the API

Warning NO AUTO RELOAD

## API

item_names = [
"Banana" =0
"Bomb" = 1
"redShroom" = 2
"goldShroom" = 3
"redShell" = 4
"blueShell" = 5
"lightning" = 6
"bulletBill" = 7
];

### update_position()

```
class Position(NamedTuple):
    name: str
    x: int
    y: int

def update_positions(positions: List[Position]) -> None:
    """
    Updates positions of players on map takes in ordered list of racers with x,y positons 1st place in 0th index 2nd place in 1st etc...
    """
```

### item_hit()

```
def item_hit(positions: List[Position]) -> None:
    """
    Updates positions of players on map takes in ordered list of racers with x,y positons 1st place in 0th index 2nd place in 1st etc...
    """
```

### item_pickup()

### item_use()
