import random

def check_cancel(lst):
    """Check if the user has cancelled the operation.

    Args:
        lst (any): User's response in list format
    returns:
        bool: True if cancelled, False otherwise
    """
    for word in lst:
        if word.lower() == "cancel":
            return True
    return False

def get_random() -> int:
    return random.randint(1000, 9999)