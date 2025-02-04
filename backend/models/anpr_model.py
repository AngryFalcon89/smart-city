from pydantic import BaseModel

class ANPRData(BaseModel):
    plate_number: str
    image: str
