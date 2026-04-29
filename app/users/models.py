from datetime import date as date_t
from enum import Enum as PyEnum

from sqlalchemy import (
    Date,
    String,
    Enum as sqlEnum,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

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

    id: Mapped[int] = mapped_column(
            primary_key=True,
            )

    username: Mapped[str] = mapped_column(
            String,
            nullable=False,
            )

    password: Mapped[str] = mapped_column(
            String,
            nullable=False,
            )

    name: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )
    email: Mapped[str] = mapped_column(
            String,
            nullable=False,
            unique=True,
            )

    phone_number: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )

    # Date : année + mois + jour  (sans heures etc)
    birth: Mapped[date_t | None] = mapped_column(
            Date,
            nullable=True,
            )

    role: Mapped[UserRoleEnum] = mapped_column(
            sqlEnum(UserRoleEnum, name="user_role_enum"),
            server_default="PATIENT",
            default=UserRoleEnum.PATIENT,
            )

    # foreign keys ========================== #

    # practitioner:
            # uselist False : empeche de retourner une liste d'objet donc mieux pour one tot one.
    practitioner_profile = relationship("Practitioner", back_populates="user_profile", uselist=False)

    # booking:
    owner_bookings = relationship("Booking", back_populates="user_profile")

    
