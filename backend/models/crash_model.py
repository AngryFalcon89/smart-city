from pydantic import BaseModel

class CrashData(BaseModel):
    filename: str
