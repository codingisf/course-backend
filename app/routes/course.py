from fastapi import APIRouter, HTTPException  # type: ignore
from app.database import db
from typing import List
from app.model import Course

router = APIRouter()

coursedb = db['courses']

@router.get("/course-list", response_model=List[Course])
async def get_all_courses():
    # Retrieve all documents from the MongoDB collection asynchronously
    courses = []
    for course in coursedb.find():
        course["_id"] = str(course["_id"])  # Convert ObjectId to string
        courses.append(Course(**course))
    
    return courses

@router.get("/course-list/{course_id}", response_model=Course)
def get_course_by_id(course_id: str): 
    # Query for a specific course by its ID
    course =  coursedb.find_one({"course_id": course_id})

    if course is None:
        raise HTTPException(status_code=404, detail="Course Not Found")
    
    return Course(**course)  # Return the course as a Course model instance
