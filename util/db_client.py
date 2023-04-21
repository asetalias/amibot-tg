import pymongo
from util import MONGO_URI, MONGO_DATABASE

client = pymongo.MongoClient(MONGO_URI)

db = client[MONGO_DATABASE]

# Adding a unique index on username
user_credentials = db["user_credentials"]
user_credentials.create_index("username", unique=True)

# Collection, use profile to create and query the db
profile = db["profile"]


