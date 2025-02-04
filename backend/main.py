from fastapi import FastAPI
from backend.routes import anpr_routes, crash_routes, face_recognition_routes
from backend.config import settings

app = FastAPI(title="Smart City Monitoring System")

# Include routes
app.include_router(anpr_routes.router, prefix="/api/anpr", tags=["ANPR"])
app.include_router(crash_routes.router, prefix="/api/crash", tags=["Crash Detection"])
app.include_router(face_recognition_routes.router, prefix="/api/face", tags=["Face Recognition"])

@app.get("/")
def root():
    return {"message": "Smart City Monitoring System API is running."}