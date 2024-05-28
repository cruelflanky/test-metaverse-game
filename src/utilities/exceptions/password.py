class PasswordDoesNotMatch(Exception):
    """
    Throw an exception when the user password does not match the entitiy's hashed password from the database.
    """
