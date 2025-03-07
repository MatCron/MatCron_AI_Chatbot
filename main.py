from fastapi import FastAPI
from pydantic import BaseModel
import CronAI
app=FastAPI()

class Account(BaseModel):
    email: str
    name: str
    token: str
    
@app.get ("/connection")
def connection():
    return {"message": "Connected"}

@app.post("/chat")
def chat():
    return {"message": "Chat"}
  