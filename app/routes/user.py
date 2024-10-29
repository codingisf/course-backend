from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from app.utils import decode_token

router = APIRouter()

@router.get('/user')
def get_user(token: str = Cookie(None)):
    if  not token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized: Token not found"})
    
    user_detail = decode_token(token)
    return user_detail
        
