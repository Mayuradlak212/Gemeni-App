import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI and database name from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Function to get a collection
def get_collection(collection_name):
    return db[collection_name]

# Test connection
if __name__ == "__main__":
    try:
        print("Connected to MongoDB:", db.name)
        print("Collections:", db.list_collection_names())
    except Exception as e:
        print("Error connecting to MongoDB:", e)
