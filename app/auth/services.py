
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security.exceptions import invalid_credentials_for_token_error_msg
from app.core.security.jwt import create_access_token
from app.core.security.pw_hashing import verify_pw
from app.core.security.schemas import BearerTokenSchema, TokenDataForCreationSchema
from app.users.models import User
from app.users.schemas import UserLoginFormSchema


async def login_service(
        user_credentials:UserLoginFormSchema,
        db: AsyncSession,
        )->BearerTokenSchema:
    """take user credentials "username" and "password", check pw and return bearer token if ok.

    Args:
        user_credentials (UserLoginFormSchema): username + password
        db (AsyncSession): database session

    Returns:
        BearerTokenSchema: Bearer token for header
    """

    result = await db.execute(select(User).where(User.username == user_credentials.username))
    user = result.scalar_one_or_none()

    if user is None:
        invalid_credentials_for_token_error_msg()
    
    if not verify_pw(user_credentials.password, user.password):
        invalid_credentials_for_token_error_msg()
    
    new_token = create_access_token(token_data=TokenDataForCreationSchema(sub=str(user.id)))

    return {
        "access_token": new_token,
        "token_type": "Bearer"
    }


