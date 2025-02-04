from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def receive_face_recognition_data(name: str, dob: str, image: str):
    return {"message": "Face recognition data received", "name": name}
