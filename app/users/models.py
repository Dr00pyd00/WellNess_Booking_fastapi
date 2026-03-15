from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Date,
    String,
    Integer,
    Enum as sqlEnum,
)

from app.core.database import Base
from app.core.models_mixins.mixin_soft_delete import SoftDeleteMixin
from app.core.models_mixins.mixin_status import StatusMixin
from app.core.models_mixins.mixin_timestamp import TimeStampMixin


class UserRoleEnum(PyEnum):

    PATIENT = "PATIENT"
    PRACTITIONER = "PRACTITIONER"
    ADMIN = "ADMIN"



class User(TimeStampMixin, StatusMixin, SoftDeleteMixin, Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,

    )

    username = Column(
        String,
        nullable=False,

    )

    name = Column(
        String,
        nullable=True,

    )

    email = Column(
        String,
        nullable=False,
        unique=True
    )

    phone_number = Column(
        String, 
        nullable=True,
    )

    # Date : année + mois + jour  (sans heures etc)
    birth = Column(
        Date,
        nullable=True,
    )

    role = Column(
        sqlEnum(UserRoleEnum, name="user_role_enum"),
        nullable=False,
        server_default=UserRoleEnum.PATIENT,
        default=UserRoleEnum.PATIENT
    )


    
