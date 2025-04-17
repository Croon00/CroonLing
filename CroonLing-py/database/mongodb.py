# from pymongo import MongoClient
from config_loader import load_config
from motor.motor_asyncio import AsyncIOMotorClient

# ✅ MongoDB Atlas 연결
config = load_config()
client = AsyncIOMotorClient(config.get('MONGO_URI'))
mongo_db = client["croonling_db"]

print("✅ MongoDB Atlas 연결 성공!")
