from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FaceRecognitionData(BaseModel):
    user_name: str
    user_photo_url: str
    is_suspected: bool
    suspicion_message: Optional[str] = None
    timestamp: datetime = datetime.now()

class FaceRecognitionResponse(BaseModel):
    id: str
    user_name: str
    user_photo_url: str
    is_suspected: bool
    suspicion_message: Optional[str] = None
    timestamp: datetime