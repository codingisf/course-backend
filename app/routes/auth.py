# app/routes/auth.py

from fastapi import APIRouter , HTTPException , status , Cookie , Response #type: ignore
from fastapi.responses import JSONResponse #type:ignore
from app.model import User , Login 
from app.database import db
from app.utils import hash_password , verify_password , create_access_token , create_refresh_token , decode_token
from datetime import datetime

router = APIRouter()


@router.post('/register')
def register(user:User):


    user_data = {
        "username": user.name,
        "email": user.email,
        "phone": user.phone,
        "passwordHash": hash_password(user.password),  # Store hashed password
        "purchasedCourses": [],  # Initialize as empty array
        "createdAt": datetime.utcnow(),  # Set creation time
    }

    db["users"].insert_one(user_data)

    return {"message" : "user registered Successfully"}



@router.post("/login")
def login(response: Response,user: Login):
    # Check if email and password are provided
    if not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required.")
    
    

    # Fetch user details from the database
    user_full_details = db["users"].find_one({"email": user.email})
    
    # Check if user exists
    if user_full_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Extract user data
    user_data = {
        "_id": str(user_full_details["_id"]),
        "email": user_full_details["email"],
        "name": user_full_details["username"]
    }
    
    # Validate the password
    is_valid = verify_password(user.password, user_full_details["passwordHash"])

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    # Generating the tokens
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    print("Tokens generated successfully.")  # Log successful token generation
    response.set_cookie(key="token",value=access_token,secure=False, 
        samesite="none",partitioned=True,httponly=True,expires=3600)
    response.set_cookie(key="refresh_token", value=access_token,secure=False, 
        samesite="none",partitioned=True, httponly=True, expires=86400)  # 1 day expiration
    response = JSONResponse(content={"message": "Login successful"})
    return{"login" :"successfully"}
    

@router.post("/refresh-token")
def refresh(response : Response,refresh_token: str = Cookie(None)):

    if not refresh_token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,details="Token is Invalid or Expired")
    
    user_details = decode_token(refresh_token)
    new_access_token = create_access_token(user_details)
    response.set_cookie(key="token",value=refresh_token,httponly=True)

    return {"access_token": str(new_access_token)}

