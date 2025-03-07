import asyncio
import websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ODk3OTQ1Zi03N2IyLTRiMjQtOGYxYS0xNzlhNjhhMGE3ZjAiLCJJZCI6Ijc4OTc5NDVmLTc3YjItNGIyNC04ZjFhLTE3OWE2OGEwYTdmMCIsIkVtYWlsIjoiam9obmRvZUBleGFtcGxlLmNvbSIsIlVzZXJUeXBlIjoiMSIsIk9yZ0lkIjoiM2UxNzYxODItYmVjYS0xMWVmLWEyNWYtMDI0MmFjMTgwMDAyIiwiZXhwIjoxNzQxNDQ1MDAxLCJpc3MiOiJNYXRjcm9uLm9ubGluZSIsImF1ZCI6Ik1hdGNyb24ub25saW5lIn0.7CRL2rrjovfR88-XVAICOrNdrcut79czHluDfMLqGoo"  # Replace with a valid JWT token
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
            print(f"Bot: {response}")

        await websocket.close()

if __name__ == "__main__":
    asyncio.run(websocket_client())
