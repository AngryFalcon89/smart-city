import os
import uuid
import logging
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from PIL import Image, UnidentifiedImageError
from backend.services.anpr_service import save_anpr_data
from backend.models.anpr_model import ANPRData, ANPRResponse

router = APIRouter()

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

@router.post("/upload", response_model=ANPRResponse)
async def upload_anpr_data(
    request: Request,
    number_plate: str = Form(...),
    image: UploadFile = File(...)
):
    logging.info("==== Received /upload request with PIL processing ====")
    logging.info(f"Image filename: {image.filename}")
    logging.info(f"Image content type: {image.content_type}")

    # Define image_path early so it's available in the exception block
    unique_filename = f"{uuid.uuid4()}_{image.filename}"
    image_path = os.path.join("uploads/anpr", unique_filename)

    try:
        # Read the entire file into memory
        image_bytes = await image.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
        # Log the first few bytes for debugging
        logging.info(f"First 20 bytes of file: {image_bytes[:20]}")

        # Create a BytesIO stream from the bytes
        image_stream = BytesIO(image_bytes)

        # Attempt to open the image with PIL
        try:
            pil_image = Image.open(image_stream)
            pil_image.load()  # Force loading the image to confirm it's valid
        except UnidentifiedImageError as pil_err:
            logging.error(f"PIL failed to open image: {pil_err}")
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        # Save the image using PIL (which properly handles image formats)
        pil_image.save(image_path)
        logging.info(f"Image saved successfully at: {image_path}")

        # Save the ANPR data
        anpr_data = ANPRData(number_plate=number_plate, image_url=image_path)
        return save_anpr_data(anpr_data)

    except HTTPException as http_ex:
        # If an HTTPException was raised (e.g., invalid image), re-raise it directly
        logging.error(f"HTTPException: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        # Remove the file if it was partially written
        if os.path.exists(image_path):
            os.remove(image_path)
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
