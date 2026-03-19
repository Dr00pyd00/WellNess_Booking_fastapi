from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Date,
    String,
    Integer,
    Enum as sqlEnum,
)
from sqlalchemy.orm import relationship

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

    password = Column(
        String,
        nullable=False
    )

    name = Column(
        String,
        nullable=True,

    )

    email = Column(
        String,
        nullable=True,
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
        server_default="PATIENT",
        default=UserRoleEnum.PATIENT
    )

    # foreign keys ========================== #

    # practitioner:
            # uselist False : empeche de retourner une liste d'objet donc mieux pour one tot one.
    practitioner_profile = relationship("Practitioner", back_populates="user_profile", uselist=False)

    # booking:
    owner_bookings = relationship("Booking", back_populates="user_profile")

    
