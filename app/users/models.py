import enum as PyEnum

from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum as sqlEnum,
)


class UserRoleEnum(PyEnum):
    PATIENT = "PATIENT"
    PRATITIONER = "PRATITIONER"
    ADMIN = "ADMIN"

    
