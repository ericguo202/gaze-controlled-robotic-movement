import asyncio
import websockets
# from robot import *
# from robot import initialize_robot, move_robot

async def handle_connection(websocket):
    print("Client connected.")
    # move_group, listener = initialize_robot()
    async for message in websocket:
        print(f"Received message: {message} with type {type(message)}")
        # move_robot(message, move_group, listener)
        await websocket.send("Got it.")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Connected to port 8765")
        await asyncio.Future() # run forever

if __name__ == "__main__": # starts server
    asyncio.run(main())

