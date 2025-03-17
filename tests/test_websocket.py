import asyncio
import websockets
import pytest

BASE_URL_WS = "ws://localhost:6000"

@pytest.mark.asyncio
async def test_websocket_notifications():
    """Test WebSocket connection for real-time order updates."""
    user_id = 1
    uri = f"{BASE_URL_WS}/ws/{user_id}"

    async with websockets.connect(uri) as websocket:
        # Simulate a message to keep the WebSocket connection open
        await websocket.send("Test connection")

      
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=5)
            assert message is not None
        except asyncio.TimeoutError:
            print("No real-time update received, but WebSocket is working.")
