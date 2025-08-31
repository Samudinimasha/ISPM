import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Database name
db = client["ispm_db"]

# Collections
users_collection = db["users"]
policies_collection = db["policies"]
training_collection = db["training"]

# Optional: Create indexes for performance
users_collection.create_index("email", unique=True)
policies_collection.create_index("title")
training_collection.create_index("title")

print("✅ MongoDB connected successfully")
