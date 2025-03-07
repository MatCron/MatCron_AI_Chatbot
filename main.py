from fastapi import FastAPI
from pydantic import BaseModel
import CronAI
import uvicorn  # Add this import

app = FastAPI()

class Account(BaseModel):
    email: str
    name: str
    token: str
    
@app.get("/connection")
def connection():
    return {"message": "Connected"}

@app.post("/chat")
def chat():
    return {"message": "Chat"}

# Add this block to run with Uvicorn
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)