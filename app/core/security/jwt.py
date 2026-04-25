from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt

from app.core.config import app_settings
from app.core.security.exceptions import invalid_token_payload_error_msg
from app.core.security.schemas import TokenDataForCreationSchema, VerifyTokenOutPutDataSchema
from app.users.models import UserRoleEnum


# Un token contient des data :
    # sub : str convention, id de l'user
    # iat : datetime, issued at, date ou on le cree
    # exp: datetime, expiration time
    # user_role : Enum



def create_access_token(
      token_data: TokenDataForCreationSchema,
      expiration_time_delta_mins:timedelta = None,
      )->str:
    """Create access jwt.

    Args:
        token_data (TokenDataForCreationSchema): 
        
            - sub (str) convention.

        expiration_time_delta_mins (timedelta, optional): perso time who want setup. Defaults to None.

    Returns:
        str: a JWT encoded with :

        - sub (str)
        - iat (datetime) issued_at
        - exp (datetime) expiration at
    """

   # time:
    now = datetime.now(timezone.utc)

    if expiration_time_delta_mins is None:
        exp_t = now + timedelta(minutes=app_settings.access_token_expire_minutes)
    else:
        exp_t = now + expiration_time_delta_mins

    to_encode = {
        "sub": token_data.sub,
        "iat": now,
        "exp": exp_t,
    }

    encoded_token = jwt.encode(
        claims=to_encode,
        key=app_settings.secret_key,
        algorithm=app_settings.algorithm
    )

    return encoded_token



def verify_jwt_token(token: str)-> VerifyTokenOutPutDataSchema:
    """check if token is valid.

    Args:
        token (str): jwt Token 

    Returns:
        VerifyTokenOutPutDataSchema:

        - user_id (int)

    """

    try:
        token_payload = jwt.decode(
            token=token,
            key=app_settings.secret_key,
            algorithms=[app_settings.algorithm]
        )

        user_id: str | None = token_payload.get("sub")
        if user_id is None :
            invalid_token_payload_error_msg()

        return VerifyTokenOutPutDataSchema(user_id=int(user_id))

    except JWTError:
        invalid_token_payload_error_msg()
    
    
    
     




