from uuid import UUID

import fastapi

from src.crud.character import CharacterCRUDInterface
from src.crud.base import get_interface
from src.schemas.routes.character import CharacterCreateType, CharacterType
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request

router = fastapi.APIRouter(prefix="/characters", tags=["characters"])


@router.post(
    path="",
    name="characters:create-character",
    response_model=CharacterType,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_character(
    character_create: CharacterCreateType,
    character_interface: CharacterCRUDInterface = fastapi.Depends(get_interface(interface_type=CharacterCRUDInterface)),
) -> CharacterType:
    new_character = await character_interface.create_character(character_create=character_create)
    return CharacterType(
        id=new_character.id,
        user_id=new_character.user_id,
        name=new_character.name,
        created_at=new_character.created_at,
    )


@router.get(
    path="/{id}",
    name="characters:read-character-by-id",
    response_model=CharacterType,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_character(
    pk: UUID,
    character_interface: CharacterCRUDInterface = fastapi.Depends(get_interface(interface_type=CharacterCRUDInterface)),
) -> CharacterType:
    try:
        db_character = await character_interface.read_character_by_id(pk=pk)
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(pk=pk)

    return CharacterType(
        id=db_character.id,
        user_id=db_character.user_id,
        name=db_character.name,
        created_at=db_character.created_at,
    )
