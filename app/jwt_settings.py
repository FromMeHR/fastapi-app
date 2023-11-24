import jwt
from fastapi import HTTPException, status

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

def encode_token(user_id: int) -> str:
    payload = {
        "user_id": user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
