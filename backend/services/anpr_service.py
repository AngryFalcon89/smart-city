from backend.models.anpr_model import ANPRData, ANPRResponse
from backend.config import settings
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(settings.DATABASE_URL)
db = client.smart_city_db
anpr_collection = db.anpr_data

def save_anpr_data(data: ANPRData):
    data_dict = data.dict()
    data_dict["timestamp"] = datetime.now()
    result = anpr_collection.insert_one(data_dict)
    return ANPRResponse(id=str(result.inserted_id), **data_dict)