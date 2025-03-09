from fastapi import HTTPException
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ISSUER = os.getenv("JWT_ISSUER")
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