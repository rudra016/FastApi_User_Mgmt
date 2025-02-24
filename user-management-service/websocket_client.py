import asyncio
import websockets
import json

WEBSOCKET_URL = "ws://localhost:6000/ws/{user_id}"  # Replace with the correct host/port

async def listen_for_updates(user_id: int):
    url = WEBSOCKET_URL.format(user_id=user_id)
    async with websockets.connect(url) as websocket:
        print(f"Connected to WebSocket for user {user_id}")

        while True:
            try:
                message = await websocket.recv()
                print(f"Received WebSocket message: {message}")
    

                # You can store this update in your database or trigger further actions
            except websockets.exceptions.ConnectionClosed:
                print(f"WebSocket disconnected for user {user_id}")
                break


asyncio.run(listen_for_updates(6))
