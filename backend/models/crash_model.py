from pydantic import BaseModel
from datetime import datetime

class CrashData(BaseModel):
    video_url: str
    location: str
    timestamp: datetime = datetime.now()

class CrashResponse(BaseModel):
    id: str
    video_url: str
    location: str
    timestamp: datetime