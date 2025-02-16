import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.services.crash_service import save_crash_data
from backend.models.crash_model import CrashData, CrashResponse

router = APIRouter()

# Ensure the uploads directory exists
os.makedirs("uploads/crash", exist_ok=True)

@router.post("/upload", response_model=CrashResponse)
async def upload_crash_data(
    location: str = Form(...),
    video: UploadFile = File(...)
):
    logging.info("==== Received /upload request for crash detection ====")
    logging.info(f"Video filename: {video.filename}")
    logging.info(f"Video content type: {video.content_type}")

    # Define video_path early so it's available in the exception block
    unique_filename = f"{uuid.uuid4()}_{video.filename}"
    video_path = os.path.join("uploads/crash", unique_filename)

    try:
        # Read the entire video file into memory
        video_bytes = await video.read()
        if not video_bytes:
            raise HTTPException(status_code=400, detail="Uploaded video is empty.")

        # Log the first few bytes for debugging
        logging.info(f"First 20 bytes of video: {video_bytes[:20]}")

        # Save the video to the uploads directory
        with open(video_path, "wb") as buffer:
            buffer.write(video_bytes)

        logging.info(f"Video saved successfully at: {video_path}")

        # Save the crash data
        crash_data = CrashData(video_url=video_path, location=location)
        return save_crash_data(crash_data)

    except HTTPException as http_ex:
        # If an HTTPException was raised (e.g., invalid video), re-raise it directly
        logging.error(f"HTTPException: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logging.error(f"Error processing video: {e}")
        # Remove the file if it was partially written
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")