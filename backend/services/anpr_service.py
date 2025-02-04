import io
from fastapi import UploadFile, HTTPException

async def process_anpr_data(plate_number: str, image: UploadFile):
    # Read the image file content
    image_content = await image.read()

    # Check if the image content is empty
    if len(image_content) == 0:
        raise HTTPException(status_code=400, detail="Empty image file")
    
    # Save the image directly as a raw file
    file_path = f"backend/uploaded_images/{plate_number}.jpg"
    with open(file_path, "wb") as f:
        f.write(image_content)
    
    return {
        "plate_number": plate_number,
        "filename": image.filename,
        "message": "Image saved successfully"
    }
