from fastapi import FastAPI, Request, HTTPException, WebSocket, Depends
import CronAI
import uvicorn
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid
import os
from dotenv import load_dotenv
import jwt
print("Main File running")
# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ISSUER = os.getenv("JWT_ISSUER")
DATABASE_URL = os.getenv("DATABASE")

# FastAPI app instance
app = FastAPI()

# Database connection
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# Database Model
class User(Base):
    __tablename__ = "Users"
    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    OrgId = Column(String(36), ForeignKey("Organisations.Id"), nullable=False)
    GroupId = Column(String(36), ForeignKey("Groups.Id"), nullable=True)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Password = Column(Text, nullable=False)
    Email = Column(String(100), nullable=True, unique=True)
    EmailVerified = Column(Boolean, nullable=False, default=False)
    UserType = Column(Integer, nullable=True)
    ProfilePicture = Column(Text, nullable=True)
    Token = Column(Text, nullable=True)

# Dependency for DB session
async def get_db():
    async with SessionLocal() as db:
        yield db

# Token validation function
def validate_request(auth_header: str):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token in Authorization header")
    token = auth_header.split("Bearer ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid token with Bearer")
    try:
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer=JWT_ISSUER,
            audience=JWT_ISSUER
        )
        return {"message": "Token is valid", "decoded": decoded_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as ex:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(ex)}")

# Routes
@app.get("/server-connection")
async def connection():
    return {"message": "Connected"}

@app.post("/validate_token")
async def validate_token(request: Request):
    auth_header = request.headers.get("Authorization")
    return {"message": validate_request(auth_header)}

@app.websocket("/ws/chatbot")
async def chatbot(websocket: WebSocket):
    try:
        auth_header = websocket.headers.get("Authorization")
        result = validate_request(auth_header)
        if not result:
            await websocket.send_text("Invalid token")
            return
    except Exception as ex:
        await websocket.send_text(str(ex))
        return
    
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "exit":
                break
            response = CronAI.chatBot(data, result["decoded"]["Email"])
            await websocket.send_text(response)
    except Exception as ex:
        await websocket.send_text(str(ex))
    finally:
        await websocket.close()

# Run the application
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
