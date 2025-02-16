from backend.models.face_recognition_model import FaceRecognitionData, FaceRecognitionResponse
from backend.config import settings
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(settings.DATABASE_URL)
db = client.smart_city_db
face_recognition_collection = db.face_recognition_data

def save_face_recognition_data(data: FaceRecognitionData):
    data_dict = data.dict()
    data_dict["timestamp"] = datetime.now()
    result = face_recognition_collection.insert_one(data_dict)
    return FaceRecognitionResponse(id=str(result.inserted_id), **data_dict)