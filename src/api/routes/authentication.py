import fastapi

from src.crud.user import UserCRUDInterface
from src.crud.base import get_interface
from src.schemas.routes.user import UserInCreateType, UserInLoginType, UserInResponseType, UserType
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.database import EntityAlreadyExists
from src.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/signup",
    name="auth:signup",
    response_model=UserInResponseType,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def signup(
    user_create: UserInCreateType,
    user_interface: UserCRUDInterface = fastapi.Depends(get_interface(interface_type=UserCRUDInterface)),
) -> UserInResponseType:
    try:
        await user_interface.is_username_taken(username=user_create.username)
        await user_interface.is_email_taken(email=user_create.email)

    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_user = await user_interface.create_user(user_create=user_create)

    return UserInResponseType(
        id=new_user.id,
        token=jwt_generator.generate_access_token(user=new_user),
        authorized_user=UserType(
            username=new_user.username,
            email=new_user.email,
            is_verified=new_user.is_verified,
            is_active=new_user.is_active,
            is_logged_in=new_user.is_logged_in,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        ),
    )


@router.post(
    path="/signin",
    name="auth:signin",
    response_model=UserInResponseType,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def signin(
    user_login: UserInLoginType,
    user_interface: UserCRUDInterface = fastapi.Depends(get_interface(interface_type=UserCRUDInterface)),
) -> UserInResponseType:
    try:
        db_user = await user_interface.read_user_by_password_authentication(user_login=user_login)

    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    return UserInResponseType(
        id=db_user.id,
        token=jwt_generator.generate_access_token(user=db_user),
        authorized_user=UserType(
            username=db_user.username,
            email=db_user.email,
            is_verified=db_user.is_verified,
            is_active=db_user.is_active,
            is_logged_in=db_user.is_logged_in,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        ),
    )
