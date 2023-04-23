import pymongo
from util.env import MONGO_URI, MONGO_DATABASE

client = pymongo.MongoClient(MONGO_URI)

db = client[MONGO_DATABASE]

# Collection, use profile to create and query the db
profile = db["profile"]
