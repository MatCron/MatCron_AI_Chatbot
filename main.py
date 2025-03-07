from fastapi import FastAPI,Request , HTTPException, Depends, WebSocket
from pydantic import BaseModel
import CronAI
import uvicorn  # Add this import
import sqlite3
import uuid
import os
from dotenv import load_dotenv
import jwtutils

# getting the values from env
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ISSUER = os.getenv("JWT_ISSUER")

# starting the application
app = FastAPI()

# connecting to the database
conn =  sqlite3.connect('user.db')
cursor = conn.cursor()

# creating the table
cursor.execute('''CREATE TABLE IF NOT EXISTS user_account (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    token TEXT NOT NULL
                )''')

# creating the user_account class
class user_account(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    token: str
    
# functions
def validate_request(request:Request ):
  auth_header = request.headers.get("Authorization")
    
  if not auth_header or not auth_header.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="Missing or invalid token")
  
  token = auth_header.split("Bearer ")[1]
  
  try:
      decoded_token, error = jwtutils.validate_token(token, JWT_SECRET, JWT_ISSUER)
      if error:
          raise HTTPException(status_code=401, detail=error)
      return decoded_token
  except Exception as ex:
    raise HTTPException(status_code=401, detail=str(ex))
    
# creating the routes
@app.get("/sever-connection")
def connection():
    return {"message": "Connected"}

@app.post("/check_account")
async def registration(user_account: user_account):
    # check if email already exists or else save to database
    await cursor.execute("SELECT * FROM user_account WHERE email = ?", (user_account.email))
    result = await cursor.fetchone()
    if result:
        return {"message": "Email already exists"}
    else:
        await cursor.execute("INSERT INTO user_account (id, email, name, token) VALUES (?, ?, ?, ?)", (str(user_account.id), user_account.email, user_account.name, user_account.token))
        await conn.commit()
        return {"message": "Account created"}
  
@app.post("/validate_token")
async def validate_token(request: Request):
    try:
        result = validate_request(request)
        return {"message": result}
    except Exception as ex:
        raise HTTPException(status_code=401, detail=str(ex))
  
@app.websocket("/ws/chatbot")
async def chatbot(websocket: WebSocket, user_account: user_account, request:Request):
  # section 1 validation
  try:
      result = validate_request(request)
      if not result:
          await websocket.send_text("Invalid token")
          return
  except Exception as ex:
      await websocket.send_text(str(ex))
      return
  # section 2 chatbot service
  try:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        if data == "exit":
            break
        else:
            response = CronAI.chatBot()
            await websocket.send_text(response)
  except Exception as ex:
      await websocket.send_text(str(ex))
  finally:
    await websocket.close()
    return


# Add this block to run with Uvicorn
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)