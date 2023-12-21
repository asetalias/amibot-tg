import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "users")
KEY = os.environ.get("KEY")
TOKEN = os.environ.get("TOKEN", "token")
URL = "amizone.fly.dev:443"
MONGO_COLLECTION = "profile"
DEV_MODE = os.environ.get("DEV_MODE", "False")
TEST_TOKEN = os.environ.get("TEST_TOKEN", "")
