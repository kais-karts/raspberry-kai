import asyncio
import json
import websockets
import threading


# Global variable to store the active websocket connection.
websocket_conn = None

async def connect_websocket(uri):
    global websocket_conn
    async with websockets.connect(uri) as websocket:
        websocket_conn = websocket  # store the connection for later use
        print(f"Connected to {uri}")
        # Optionally, you can have a task here that handles incoming messages.
        await handle_communication(websocket)
        # When handle_communication() returns, the connection will close.
        websocket_conn = None

async def handle_communication(websocket):
    """
    Example communication loop that lets you send messages from the console.
    """
    while True:
        # Note: input() is blocking. Here we run it in an executor so it doesn't block the event loop.
        message = await asyncio.get_event_loop().run_in_executor(None, input, "Enter message to send (or 'exit'): ")
        if message.lower() == 'exit':
            break
        print("imma send ", message, " to ", websocket_conn)
        # out = await websocket_conn.recv()
        # print("i got", out)
        await websocket_conn.send(message)

# Now define the item functions as async functions.
async def item_pickup(item: int, x, y) -> None:
    """
    Updates the UI when a new item is picked up by sending a message over the websocket.
    """
    if websocket_conn is None:
        print("No active websocket connection.")
        return

    # Create a message (you can design your own JSON format)
    msg = json.dumps({
        "action": "item_pickup",
        "item": item,
        "x": x,
        "y": y
    })
    await websocket_conn.send(msg)
    print(f"Sent item_pickup: {msg}")

async def item_hit(item: int,  x, y) -> None:
    """
    Updates the UI when the player is hit with an item.
    """
    if websocket_conn is None:
        print("No active websocket connection.")
        return

    msg = json.dumps({
        "action": "item_hit",
        "item": item,
        "x": x,
        "y": y
    })
    await websocket_conn.send(msg)
    print(f"Sent item_hit: {msg}")

async def item_use(duration: float, x, y) -> None:
    """
    Updates the UI when the player uses an item.
    """
    if websocket_conn is None:
        print("No active websocket connection.")
        return

    msg = json.dumps({
        "action": "item_use",
        "duration": duration,
        "x": x,
        "y": y
    })
    await websocket_conn.send(msg)
    print(f"Sent item_use: {msg}")




async def hello(websocket, path):
    global websocket_conn
    websocket_conn = websocket
    while True:
        pass
    # while True:
    #     await websocket.send("Connect")




# Example of how you might call these functions from within your asyncio event loop:
def init():
    uri = "ws://localhost:5000"  # Replace with your WebSocket server URI
    # # Start the websocket connection in a background task.
    # ws_task = connect_websocket(uri)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(hello, "localhost", 5000)
    loop.run_until_complete(start_server)
    loop.run_forever()
    # global websocket_conn
    # async with websockets.serve(echo, "localhost", 8080) as server:
    #     print("here", server)
    #     websocket_conn = server
    #     await server.serve_forever()
    # # ws_task = asyncio.run(connect_websocket(uri))
    # # Wait a moment to ensure the connection is established.
    # await asyncio.sleep(1)
