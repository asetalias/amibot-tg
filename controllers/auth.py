from util.db_client import profile


def create_profile(telegram_id, username, password) -> str:
    data = {"_id": telegram_id, "username": username, "password": password}

    try:
        profile.insert_one(data)
        return "Profile created successfully"
    except Exception as e:
        return str(e)


def get_profile(telegram_id) -> dict:
    try:
        data = profile.find_one({"_id": telegram_id})
        return data
    except Exception as e:
        return str(e)


def update_profile(telegram_id, username, password) -> str:
    try:
        filter = {"_id": telegram_id}
        update = {"$set": {"username": username, "password": password}}
        profile.update_one(filter, update)
        return "Profile updated successfully"
    except Exception as e:
        return str(e)


def delete_profile(telegram_id) -> str:
    try:
        profile.delete_one({"_id": telegram_id})
        return "Profile deleted successfully"
    except Exception as e:
        return str(e)
