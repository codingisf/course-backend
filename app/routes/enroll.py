from fastapi import APIRouter, HTTPException, Cookie, status , Request  # type: ignore
from app.database import db
from bson import ObjectId  # type: ignore
from app.model import Enrollment_Request
from app.utils import decode_token

router = APIRouter()

@router.post('/enroll', status_code=status.HTTP_200_OK)
def course_enrollment(
    request: Request,
    enrollment: Enrollment_Request,
    token : str = Cookie(None),
):
    # Decode the token to get user info
    print("Token from cookie:", request.cookies) 

    current_user = decode_token(token) 
    
    # Check if current_user is None (i.e., token is invalid or expired)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    print(current_user)
    print("It's enrolling")
    print(enrollment)
    user_id = current_user["_id"]
    total_chapters = 10  # Example: Can be dynamic based on the course
    print(enrollment.course_id)
    
    # Prepare the course object
    course = {
        "course_id": enrollment.course_id,
        "progress": {"completedChapters": 0, "totalChapters": total_chapters}
    }

    # Fetch the user
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user is already enrolled in the course
    if any(c["course_id"] == enrollment.course_id for c in user.get("purchasedCourses", [])):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )

    # Enroll the user in the course by adding it to purchasedCourses
    result = db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"purchasedCourses": course}}
    )

    # Verify if the update was successful
    if result.modified_count == 0:
        raise HTTPException(
            status_code=500, detail="Failed to enroll in the course"
        )

    return {"message": "Successfully enrolled", "course_id": enrollment.course_id}
