from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from backend.config import settings

uri =  settings.DATABASE_URL

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.smart_city_db

# Create collections
db.create_collection("anpr_data")
db.create_collection("crash_data")
db.create_collection("face_recognition_data")

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)