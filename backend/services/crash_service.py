from backend.models.crash_model import CrashData, CrashResponse
from backend.config import settings
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(settings.DATABASE_URL)
db = client.smart_city_db
crash_collection = db.crash_data

def save_crash_data(data: CrashData):
    data_dict = data.dict()
    data_dict["timestamp"] = datetime.now()
    result = crash_collection.insert_one(data_dict)
    return CrashResponse(id=str(result.inserted_id), **data_dict)