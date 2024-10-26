# app/main.py
from fastapi import FastAPI 
from app.routes import auth, course , enroll , progress
from fastapi.middleware.cors import CORSMiddleware # from app.JWT_middleware import AuthenticateRequest
import os
import uvicorn 





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin","Set-Cookie"],  # Allow all headers (including Authorization, Content-Type)
)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(course.router, prefix="/course", tags=["Courses"])
app.include_router(enroll.router,prefix="/dashboard", tags=["Enroll"])
app.include_router(progress.router,prefix="/dashboard", tags=["[progress]"])

@app.get("/")
def root():
    return {"message": "Welcome to the Course API!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use PORT env variable or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
