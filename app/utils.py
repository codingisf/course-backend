# app/utils.py

from passlib.context import CryptContext # type: ignore
from fastapi import HTTPException , status ,Header # type: ignore
from jose import jwt #type: ignore
from datetime import datetime, timedelta
from dotenv import load_dotenv #type: ignore
import os
from typing import Optional

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# this funtion will create both access and refresh tokens
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password)
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_valid = pwd_context.verify(plain_password, hashed_password)
    return is_valid

    
def create_access_token(data:dict):
    return create_token(data,timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data:dict):
    return create_token(data,timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        return payload
    
    except JWTError: #type: ignore
        return None


def decode_token(authorization:Optional[str]):
    # Check if the Authorization header is present
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    print(authorization)
    try:

        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User details not provided in the token or token expired"
            )

        return payload  # Return the decoded payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
        