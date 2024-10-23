from fastapi import APIRouter, HTTPException #type: ignore
from bson import ObjectId #type: ignore
from bson.errors import InvalidId #type: ignore
from app.model import ProgressUpdateRequest
from app.database import db

router = APIRouter()

# Assuming ProgressUpdateRequest is defined elsewhere
@router.post("/course/progress")
def update_course_progress(
    request: ProgressUpdateRequest
):
    try:
        user_id = ObjectId(request.user_id)  # Convert to ObjectId
        course_id = request.course_id  # Ensure course_id is an ObjectId
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Query to find the user and the course inside purchasedCourses
    query = {
        "_id": user_id,
        "purchasedCourses.course_id": course_id
    }
    # Update data to set completed chapters
    update_data = {
        "$set": {
            "purchasedCourses.$.progress.completedChapters": request.completed_chapter
        }
    }

    # Perform the update operation
    result = db["users"].update_one(query, update_data)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User or course not found")

    return {"message": "Progress updated successfully"}