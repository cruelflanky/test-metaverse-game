from datetime import datetime, timedelta, UTC

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from src.config.manager import settings
from src.models.user import User
from src.schemas.jwt import JWTUser, JWToken
from src.utilities.exceptions.database import EntityDoesNotExist


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = jwt_data.copy()

        if expires_delta:
            expire = datetime.now(UTC) + expires_delta

        else:
            expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_MIN)

        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())

        return jose_jwt.encode(to_encode, key=settings.JWT_SECRET_KEY_ACCESS_TOKEN, algorithm=settings.JWT_ALGORITHM)

    def generate_access_token(self, user: User) -> str:
        if not user:
            raise EntityDoesNotExist(f"Cannot generate JWT token without User entity!")

        return self._generate_jwt_token(
            jwt_data=JWTUser(user_id=user.id, email=user.email).dict(),
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME_MIN),
        )

    def generate_refresh_token(self, user: User) -> str:
        if not user:
            raise EntityDoesNotExist(f"Cannot generate JWT token without User entity!")

        return self._generate_jwt_token(
            jwt_data=JWTUser(user_id=user.id, email=user.email).dict(),
            expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRATION_TIME_DAYS),
        )

    def retrieve_details_from_token(self, token: str, secret_key: str) -> JWTUser:
        try:
            payload = jose_jwt.decode(token=token, key=secret_key, algorithms=[settings.JWT_ALGORITHM])
            jwt_user = JWTUser(user_id=payload["user_id"], email=payload["email"])

        except JoseJWTError as token_decode_error:
            raise ValueError("Unable to decode JWT Token") from token_decode_error

        except pydantic.ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        return jwt_user


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
