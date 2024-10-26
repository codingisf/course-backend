# app/models.py

from pydantic import BaseModel , EmailStr , Field # type: ignore
from typing import List,Optional

class User(BaseModel):
    name : str
    phone: int
    email : EmailStr
    password : str

class Course(BaseModel):
    course_id: str #type: ignore
    title: str
    description: str
    price: float
    duration: str
    instructor: Optional[str] = Field(default=None) 

class Login(BaseModel):
    email:EmailStr
    password:str

class Enrollment_Request(BaseModel):
    course_id : str

class userModel(BaseModel):
    Student_id : str
    Enrollments : List[str]

class ProgressUpdateRequest(BaseModel):
    user_id: str
    course_id: str
    completed_chapter: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class cookieModel(BaseModel):
    token:str
    RefreshToken:str
