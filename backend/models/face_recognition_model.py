from pydantic import BaseModel

class FaceRecognitionData(BaseModel):
    name: str
    dob: str
    image: str