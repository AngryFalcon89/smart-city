from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
def receive_crash_data(file: UploadFile = File(...)):
    return {"message": "Crash data received", "filename": file.filename}