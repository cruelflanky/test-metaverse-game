"""
The HyperText Transfer Protocol (HTTP) 401 Unauthorized response status code indicates that the client
request has not been completed because it lacks valid authentication credentials for the requested resource.
"""

import fastapi

from src.utilities.messages.exceptions.http.exc_details import (
    http_401_token_credentials_details,
    http_401_token_expired_details,
)


async def http_401_token_credentials_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail=http_401_token_credentials_details(),
    )


async def http_401_token_expired_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail=http_401_token_expired_details(),
    )
