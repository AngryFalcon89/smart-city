import os
import uuid
import logging
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image, UnidentifiedImageError
from backend.services.face_recognition_service import save_face_recognition_data
from backend.models.face_recognition_model import FaceRecognitionData, FaceRecognitionResponse

router = APIRouter()

# Ensure the uploads directory exists
os.makedirs("uploads/face_recognition", exist_ok=True)

@router.post("/upload", response_model=FaceRecognitionResponse)
async def upload_face_recognition_data(
    user_name: str = Form(...),
    user_photo: UploadFile = File(...),
    is_suspected: bool = Form(...),
    suspicion_message: str = Form(None)
):
    logging.info("==== Received /upload request for face recognition ====")
    logging.info(f"User photo filename: {user_photo.filename}")
    logging.info(f"User photo content type: {user_photo.content_type}")
    logging.info(f"User name: {user_name}")
    logging.info(f"Is suspected: {is_suspected}")
    logging.info(f"Suspicion message: {suspicion_message}")

    # Define photo_path early so it's available in the exception block
    unique_filename = f"{uuid.uuid4()}_{user_photo.filename}"
    photo_path = os.path.join("uploads/face_recognition", unique_filename)

    try:
        # Read the entire photo file into memory
        photo_bytes = await user_photo.read()
        if not photo_bytes:
            raise HTTPException(status_code=400, detail="Uploaded photo is empty.")

        # Log the first few bytes for debugging
        logging.info(f"First 20 bytes of photo: {photo_bytes[:20]}")

        # Create a BytesIO stream from the bytes
        photo_stream = BytesIO(photo_bytes)

        # Attempt to open the image with PIL
        try:
            pil_image = Image.open(photo_stream)
            pil_image.load()  # Force loading the image to confirm it's valid
        except UnidentifiedImageError as pil_err:
            logging.error(f"PIL failed to open image: {pil_err}")
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        # Save the image using PIL (which properly handles image formats)
        pil_image.save(photo_path)
        logging.info(f"User photo saved successfully at: {photo_path}")

        # Save the face recognition data
        face_data = FaceRecognitionData(
            user_name=user_name,
            user_photo_url=photo_path,
            is_suspected=is_suspected,
            suspicion_message=suspicion_message
        )
        return save_face_recognition_data(face_data)

    except HTTPException as http_ex:
        # If an HTTPException was raised (e.g., invalid image), re-raise it directly
        logging.error(f"HTTPException: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logging.error(f"Error processing user photo: {e}")
        # Remove the file if it was partially written
        if os.path.exists(photo_path):
            os.remove(photo_path)
        raise HTTPException(status_code=500, detail=f"Error processing user photo: {str(e)}")