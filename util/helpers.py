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
