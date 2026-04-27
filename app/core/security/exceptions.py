
from typing import Never

from fastapi import HTTPException, status


def invalid_token_payload_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token Credentials."
    )


def invalid_credentials_for_token_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid JWT Credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
