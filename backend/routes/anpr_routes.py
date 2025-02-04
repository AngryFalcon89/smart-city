from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.services.anpr_service import process_anpr_data

router = APIRouter()

@router.post("/")
async def receive_anpr_data(plate_number: str = Form(...), image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="Image file is required")
    
    result = await process_anpr_data(plate_number, image)
    return result
