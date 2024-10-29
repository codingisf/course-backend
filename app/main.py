# app/main.py
from fastapi import FastAPI 
from app.routes import auth, course , enroll , progress , user
from fastapi.middleware.cors import CORSMiddleware # from app.JWT_middleware import AuthenticateRequest
import os
import uvicorn 





app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers (including Authorization, Content-Type)
)


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(course.router, prefix="/course", tags=["Courses"])
app.include_router(enroll.router,prefix="/dashboard", tags=["Enroll"])
app.include_router(progress.router,prefix="/dashboard", tags=["[progress]"])
app.include_router(user.router, tags=["[user]"])

@app.get("/")
def root():
    return {"message": "Welcome to the Course API!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use PORT env variable or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
