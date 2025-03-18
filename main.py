from fastapi import FastAPI, Depends, HTTPException, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from Service.baseFunction import validate_request
from Service.database import get_db
from Service.schemas import UserOut
from Service.crud import get_user_by_id, get_users
import Service.cronAI as cronAI
import uvicorn
import json
from datetime import datetime

app = FastAPI()

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: str, db: AsyncSession = Depends(get_db)):
    print("User ID:", user_id)
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users")
async def get_users_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        users = await get_users(db, skip, limit)
        print("Users:", users)
        return users
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@app.get("/server-connection")
async def connection():
    return {"message": "Connected"}
  
@app.get("/test-token")
async def test_token(request : Request,db: AsyncSession = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    result = validate_request(auth_header)
    print(f"Token validation result: {result}")
    users = await get_user_by_id(db, result["decoded"]["Id"])
    print(f"User lookup result: {users}") 
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users

@app.websocket("/ws/chatbot")
async def chatbot(websocket: WebSocket,db: AsyncSession = Depends(get_db)):
    try:
        await websocket.accept()
        auth_header = websocket.headers.get("Authorization")
        result = validate_request(auth_header)
        print(f"Token validation result: {result}")
        if not result:
            await websocket.send_text("Invalid token")
            return
        
        users = await get_user_by_id(db, result["decoded"]["Id"])
        if users is None:
            raise Exception(status_code=404, detail="User not found")
        if users.Email != result["decoded"]["Email"]:
            raise Exception(status_code=401, detail="Invalid token Email")
        if users.OrgId != result["decoded"]["OrgId"]:
            raise Exception(status_code=401, detail="Token Error Org")
        
    except Exception as ex:
        await websocket.send_text(str(ex))
        return
    
    
    try:
        while True:
            data = await websocket.receive_text()
            if data == "exit":
                break
            response = cronAI.chatBot(data, result["decoded"]["Email"])
            await websocket.send_text(json.dumps({"message":response,
            "status": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}))
    except Exception as ex:
        await websocket.send_text(str(ex))
    finally:
        await websocket.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
