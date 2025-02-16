from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import anpr_routes, crash_routes, face_recognition_routes

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(anpr_routes.router, prefix="/api/anpr", tags=["ANPR"])
app.include_router(crash_routes.router, prefix="/api/crash", tags=["Crash Detection"])
app.include_router(face_recognition_routes.router, prefix="/api/face-recognition", tags=["Face Recognition"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart City Backend API"}