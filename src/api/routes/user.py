from uuid import UUID

import fastapi
import pydantic

from src.crud.user import UserCRUDInterface
from src.crud.base import get_interface
from src.schemas.routes.user import UserInResponseType, UserInUpdateType, UserType
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="",
    name="users:read-users",
    response_model=list[UserInResponseType],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_users(
    user_interface: UserCRUDInterface = fastapi.Depends(get_interface(interface_type=UserCRUDInterface)),
) -> list[UserInResponseType]:
    db_users = await user_interface.read_users()
    db_user_list: list = list()

    for db_user in db_users:
        access_token = jwt_generator.generate_access_token(user=db_user)
        user = UserInResponseType(
            id=db_user.id,
            authorized_user=UserType(
                token=access_token,
                username=db_user.username,
                email=db_user.email,
                is_verified=db_user.is_verified,
                is_active=db_user.is_active,
                is_logged_in=db_user.is_logged_in,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
            ),
        )
        db_user_list.append(user)

    return db_user_list


@router.get(
    path="/{id}",
    name="users:read-user-by-id",
    response_model=UserInResponseType,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user(
    pk: UUID,
    user_interface: UserCRUDInterface = fastapi.Depends(get_interface(interface_type=UserCRUDInterface)),
) -> UserInResponseType:
    try:
        db_user = await user_interface.read_user_by_id(pk=pk)
        access_token = jwt_generator.generate_access_token(user=db_user)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(pk=pk)

    return UserInResponseType(
        id=db_user.id,
        authorized_user=UserType(
            token=access_token,
            username=db_user.username,
            email=db_user.email,  # type: ignore
            is_verified=db_user.is_verified,
            is_active=db_user.is_active,
            is_logged_in=db_user.is_logged_in,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        ),
    )


@router.patch(
    path="/{id}",
    name="users:update-user-by-id",
    response_model=UserInResponseType,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_user(
    query_id: UUID,
    update_username: str | None = None,
    update_email: pydantic.EmailStr | None = None,
    update_password: str | None = None,
    user_interface: UserCRUDInterface = fastapi.Depends(get_interface(interface_type=UserCRUDInterface)),
) -> UserInResponseType:
    user_update = UserInUpdateType(username=update_username, email=update_email, password=update_password)
    try:
        updated_db_user = await user_interface.update_user_by_id(pk=query_id, user_update=user_update)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(pk=query_id)

    access_token = jwt_generator.generate_access_token(user=updated_db_user)

    return UserInResponseType(
        id=updated_db_user.id,
        authorized_user=UserType(
            token=access_token,
            username=updated_db_user.username,
            email=updated_db_user.email,  # type: ignore
            is_verified=updated_db_user.is_verified,
            is_active=updated_db_user.is_active,
            is_logged_in=updated_db_user.is_logged_in,
            created_at=updated_db_user.created_at,
            updated_at=updated_db_user.updated_at,
        ),
    )


@router.delete(path="", name="users:delete-user-by-id", status_code=fastapi.status.HTTP_200_OK)
async def delete_user(
    pk: UUID,
    user_interface: UserCRUDInterface = fastapi.Depends(get_interface(interface_type=UserCRUDInterface)),
) -> dict[str, str]:
    try:
        deletion_result = await user_interface.delete_user_by_id(pk=pk)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(pk=pk)

    return {"notification": deletion_result}
