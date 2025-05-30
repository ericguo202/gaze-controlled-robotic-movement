import asyncio
import websockets
from robot import *
from robot import main as main2
async def handle_connection(websocket):
    print("Client connected.")
    async for message in websocket:
        print(f"Received message: {message}")
        main2(message)
        await websocket.send("Got it.")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Connected to port 8765")
        await asyncio.Future() # run forever

if __name__ == "__main__": # starts server
    asyncio.run(main())

