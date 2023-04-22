from util.db_client import profile

def create_profile(username, password) -> str:
    data = {
        "username": username,
        "password": password
    }

    try :
        profile.insert_one(data)
        return "Profile created successfully"
    except Exception as e:
        return str(e)
    

def get_profile(username) -> dict:
    try:
        data = profile.find_one({"username": username})
        return data
    except Exception as e:
        return str(e)
    

def update_profile(username, password) -> str:
    try:
        profile.update_one({"username": username}, {"$set": {"password": password}})
        return "Profile updated successfully"
    except Exception as e:
        return str(e)

def delete_profile(username) -> str:
    try:
        profile.delete_one({"username": username})
        return "Profile deleted successfully"
    except Exception as e:
        return str(e)