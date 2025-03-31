import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ODk3OTQ1Zi03N2IyLTRiMjQtOGYxYS0xNzlhNjhhMGE3ZjAiLCJJZCI6Ijc4OTc5NDVmLTc3YjItNGIyNC04ZjFhLTE3OWE2OGEwYTdmMCIsIkVtYWlsIjoiam9obmRvZUBleGFtcGxlLmNvbSIsIlVzZXJUeXBlIjoiMSIsIk9yZ0lkIjoiM2UxNzYxODItYmVjYS0xMWVmLWEyNWYtMDI0MmFjMTgwMDAyIiwiT3JnVHlwZSI6IjAiLCJleHAiOjE3NDQwMjk5NjEsImlzcyI6Ik1hdGNyb24ub25saW5lIiwiYXVkIjoiTWF0Y3Jvbi5vbmxpbmUifQ.mIlIT9b8PqX3Ib5GoXtrufw0mzs3vC9loe9BpzPTRT0"
WS_URL = "ws://localhost:8000/ws/chatbot"

async def websocket_client():
    headers = {"Authorization": f"Bearer {TOKEN}"}

    async with websockets.connect(WS_URL, extra_headers=headers) as websocket:
        print("Connected to the chatbot WebSocket")
        
        response = await websocket.recv()
        response = json.loads(response)
        if response["status"] == "failed":
                print(f"Bot: {response['message']}")
                return
        else :
            print(f"Bot: {response['message']}")
        while True:
            message = input("You: ")
            if message.lower() == "exit":
                print("Closing connection...")
                break
            jsonMessage = json.dumps({"message": message})
            await websocket.send(jsonMessage)
            response = await websocket.recv()
            message = json.loads(response)["message"]
            print(f"Bot: {message}")

        await websocket.close()

if __name__ == "__main__":
    asyncio.run(websocket_client())

