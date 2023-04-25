from util.db_client import profile


async def create_profile(telegram_id: int, username, password) -> str:
    data = {"_id": telegram_id, "username": username, "password": password}

    try:
        await profile.insert_one(data)
        return "Profile created successfully"
    except Exception as e:
        return str(e)


async def get_profile(telegram_id: int) -> dict:
    try:
        data = await profile.find_one({"_id": telegram_id})
        return data
    except Exception as e:
        print(e)
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
