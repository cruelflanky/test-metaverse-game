from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CharacterCreateType(BaseModel):
    user_id: UUID
    name: str


class CharacterType(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime
