from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv
import os


# Global MongoDB client and database instances
mongo_client: Optional[AsyncIOMotorClient] = None
database = None

load_dotenv()

async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    global mongo_client, database
    
    # MongoDB connection string - update with your credentials
    MONGODB_URL = os.getenv("MONGODB_URL")
    
    mongo_client = AsyncIOMotorClient(MONGODB_URL)
    database = mongo_client.content_ai_db
    
    print("✅ Connected to MongoDB - Database: content_ai_db")


async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    global mongo_client
    
    if mongo_client:
        mongo_client.close()
        print("❌ MongoDB connection closed")


def get_database():
    """Get database instance"""
    return database
