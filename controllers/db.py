from util.db_client import profile
from util.encryption import encrypt, decrypt
import logging

logger = logging.getLogger()


async def checkToken(telegram_id: int, token: int) -> bool:
    try:
        logger.info("Checking token")
        data = await profile.find_one({"token": token})
        if data == None:
            logger.info("Setting token")
            val = await setToken(telegram_id, token)
            if val:
                return True
            else:
                return False
        return False
    except Exception as e:
        print(e)
        return False


async def setToken(telegram_id: int, token: int) -> bool:
    try:
        filter = {"_id": telegram_id}
        update = {"$set": {"token": token}}
        await profile.update_one(filter, update)
        return True
    except Exception as e:
        logger.error(e)
        return False


async def create_profile(telegram_id: int, username, password) -> str:
    data = await profile.find_one({"_id": telegram_id})
    if data != None:
        encrypted_password = encrypt(password)
        resp = await update_profile(telegram_id, username, encrypted_password)
        return resp

    encrypted_password = encrypt(password)
    data = {"_id": telegram_id, "username": username, "password": encrypted_password}

    try:
        await profile.insert_one(data)
        return "Profile created successfully"
    except Exception as e:
        return str(e)


async def get_profile_via_token(token: int) -> dict | None:
    try:
        logger.info("Getting profile")
        data = await profile.find_one({"token": token})
        data["password"] = decrypt(data["password"])
        return data
    except Exception as e:
        print(e)
        return None


async def get_profile(telegram_id: int) -> dict:
    try:
        logger.info("Getting profile")
        data = await profile.find_one({"_id": telegram_id})
        data["password"] = decrypt(data["password"])
        return data
    except Exception as e:
        logger.error(e)
        return str(e)


async def update_profile(telegram_id: int, username, password) -> str:
    try:
        filter = {"_id": telegram_id}
        update = {"$set": {"username": username, "password": password}}
        await profile.update_one(filter, update)
        return "Profile updated successfully"
    except Exception as e:
        return str(e)


async def delete_profile(telegram_id: int) -> str:
    try:
        await profile.delete_one({"_id": telegram_id})
        return "Profile deleted successfully"
    except Exception as e:
        return str(e)
