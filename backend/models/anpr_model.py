from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ANPRData(BaseModel):
    number_plate: str
    image_url: str
    timestamp: datetime = datetime.now()

class ANPRResponse(BaseModel):
    id: str
    number_plate: str
    image_url: str
    timestamp: datetime