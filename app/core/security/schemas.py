from pydantic import BaseModel

from app.users.models import UserRoleEnum


class TokenDataForCreationSchema(BaseModel):
    sub: str
    user_role: UserRoleEnum