# app/database.py

import os
from dotenv import load_dotenv # type: ignore
from pymongo.mongo_client import MongoClient # type: ignore

load_dotenv()

client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

db = client["course-database"]

try:
    client.server_info()  # Will throw an error if unable to connect
    print("Connection successful")
except Exception as e:
    print("Connection failed:", e)
