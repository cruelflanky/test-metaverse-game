from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from src.schemas.base import BaseSchemaModel


class UserInCreateType(BaseSchemaModel):
    username: str
    email: EmailStr
    password: str


class UserInUpdateType(BaseSchemaModel):
    username: str | None
    email: str | None
    password: str | None


class UserInLoginType(BaseSchemaModel):
    email: EmailStr
    password: str


class UserType(BaseSchemaModel):
    username: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    is_logged_in: bool
    created_at: datetime
    updated_at: datetime | None


class UserInResponseType(BaseSchemaModel):
    id: UUID
    token: str
    authorized_user: UserType
