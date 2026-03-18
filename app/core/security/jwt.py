from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt

from app.core.config import app_settings
from app.core.security.schemas import TokenDataForCreationSchema


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
            - user_role (UserRoleEnum) 

        expiration_time_delta_mins (timedelta, optional): perso time who want setup. Defaults to None.

    Returns:
        str: a JWT encoded with :

        - sub (str)
        - user_role (UserRoleEnum)
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
        "user_role": token_data.user_role,
        "iat": now,
        "exp": exp_t,
    }

    encoded_token = jwt.encode(
        claims=to_encode,
        key=app_settings.secret_key,
        algorithm=app_settings.algorithm
    )

    return encoded_token

    
    
    
     





# create token with data.