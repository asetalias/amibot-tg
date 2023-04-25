# import pymongo
# from util.env import MONGO_URI, MONGO_DATABASE

# client = pymongo.MongoClient(MONGO_URI)

# db = client[MONGO_DATABASE]

# # Collection, use profile to create and query the db
# profile = db["profile"]

import asyncio
import motor.motor_asyncio
from util.env import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DATABASE]
profile = db[MONGO_COLLECTION]
