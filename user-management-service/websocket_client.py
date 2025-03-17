import asyncio
import websockets


WEBSOCKET_URL = "ws://localhost:6000/ws/{user_id}"  

async def listen_for_updates(user_id: int):
    """Connects to WebSocket and listens for messages."""
    url = WEBSOCKET_URL.format(user_id=user_id)

    while True: 
        try:
            async with websockets.connect(url) as websocket:
                print(f"Connected to WebSocket for user {user_id}")

                while True:
                    message = await websocket.recv()
                    print(f"Received WebSocket message: {message}")

        except websockets.exceptions.ConnectionClosed:
            print(f"WebSocket disconnected for user {user_id}, retrying in 3 seconds...")
            await asyncio.sleep(3)  

asyncio.run(listen_for_updates(7))
