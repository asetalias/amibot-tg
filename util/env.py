import os
from dotenv import load_dotenv

dev_mode = False

if dev_mode:
    load_dotenv("dev.env")
else:
    load_dotenv("app.env")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "users")
KEY = os.environ.get("KEY")
TOKEN = os.environ.get("TOKEN", "token")
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
URL = "amizone.fly.dev:443"
MONGO_COLLECTION = "profile"

