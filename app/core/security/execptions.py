


from fastapi import HTTPException, status


def invalid_token_payload_error_msg():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token Credentials."
    )

