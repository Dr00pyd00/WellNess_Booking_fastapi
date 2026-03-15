import enum as PyEnum

from sqlalchemy import (

)


class UserRoleEnum(PyEnum):
    PATIENT = "PATIENT"
    PRATITIONER = "PRATITIONER"
    ADMIN = "ADMIN"

    