import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ODk3OTQ1Zi03N2IyLTRiMjQtOGYxYS0xNzlhNjhhMGE3ZjAiLCJJZCI6Ijc4OTc5NDVmLTc3YjItNGIyNC04ZjFhLTE3OWE2OGEwYTdmMCIsIkVtYWlsIjoiam9obmRvZUBleGFtcGxlLmNvbSIsIlVzZXJUeXBlIjoiMSIsIk9yZ0lkIjoiM2UxNzYxODItYmVjYS0xMWVmLWEyNWYtMDI0MmFjMTgwMDAyIiwiT3JnVHlwZSI6IlVua25vd24iLCJleHAiOjE3NDI2OTg0ODgsImlzcyI6Ik1hdGNyb24ub25saW5lIiwiYXVkIjoiTWF0Y3Jvbi5vbmxpbmUifQ.TPOaaNwwe8-pMS4b6msBINda0XeAA9hLskjWmCKRCOk"  # Replace with a valid JWT token
WS_URL = "ws://localhost:8000/ws/chatbot"

async def websocket_client():
    headers = {"Authorization": f"Bearer {TOKEN}"}

    async with websockets.connect(WS_URL, extra_headers=headers) as websocket:
        print("Connected to the chatbot WebSocket")

        while True:
            message = input("You: ")
            if message.lower() == "exit":
                print("Closing connection...")
                break

            await websocket.send(message)
            response = await websocket.recv()
            message = json.loads(response)["message"]
            print(f"Bot: {message}")

        await websocket.close()

if __name__ == "__main__":
    asyncio.run(websocket_client())
