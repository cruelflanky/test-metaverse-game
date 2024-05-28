from uuid import UUID


def http_400_username_details(username: str) -> str:
    return f"The username {username} is taken! Be creative and choose another one!"


def http_400_email_details(email: str) -> str:
    return f"The email {email} is already registered! Be creative and choose another one!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed! Recheck all your credentials!"


def http_400_sigin_credentials_details() -> str:
    return "Signin failed! Recheck all your credentials!"


def http_401_token_credentials_details() -> str:
    return "Invalid authentication scheme. Provide valid credentials."


def http_401_token_expired_details() -> str:
    return "Token has expired. Please sign in again!"


def http_403_forbidden_details() -> str:
    return "Refused access to the requested resource!"


def http_404_id_details(pk: UUID) -> str:
    return f"Either the user with id `{pk}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_username_details(username: str) -> str:
    return f"Either the user with username `{username}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_email_details(email: str) -> str:
    return f"Either the user with email `{email}` doesn't exist, has been deleted, or you are not authorized!"
