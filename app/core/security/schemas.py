from pydantic import BaseModel

from app.users.models import UserRoleEnum


class TokenDataForCreationSchema(BaseModel):
    sub: str


class VerifyTokenOutPutDataSchema(BaseModel):
    user_id: int