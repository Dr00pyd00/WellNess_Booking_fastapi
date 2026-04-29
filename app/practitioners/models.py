from enum import Enum as PyEnum

from decimal import Decimal # mieux pour les prix, plus precis

from sqlalchemy import (
    Boolean,
    Numeric,
    Enum as sqlEnum,
    text,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base
from app.core.models_mixins.mixin_soft_delete import SoftDeleteMixin
from app.core.models_mixins.mixin_status import StatusMixin
from app.core.models_mixins.mixin_timestamp import TimeStampMixin



class PractitionerSpecialtyEnum(PyEnum):
    OSTEOPATH = "OSTEOPATH"
    PHYSIOTHERAPIST = "PHYSIOTHERAPIST"
    PSYCHOLOGIST = "PSYCHOLOGIST"
    NATUROPATH = "NATUROPATH"
    NUTRITIONIST = "NUTRITIONIST"
    YOGA_INSTRUCTOR = "YOGA_INSTRUCTOR"
    SPORT_COACH = "SPORT_COACH"
    ACUPUNCTURIST = "ACUPUNCTURIST"
    MASSAGE_THERAPIST = "MASSAGE_THERAPIST"
    OTHER = "OTHER"



class Practitioner(TimeStampMixin, StatusMixin, SoftDeleteMixin, Base):

    __tablename__= 'practitioners'

    id: Mapped[int] = mapped_column(
            primary_key=True,
            )

    speciality: Mapped[PractitionerSpecialtyEnum] = mapped_column(
            sqlEnum(PractitionerSpecialtyEnum, name="practitioner_speciality_enum"),
            )

    # consult a distance
    is_remote_possible: Mapped[bool] = mapped_column(
            Boolean,
            server_default=text("False"),
            default=False,
            )
    
    address: Mapped[str] = mapped_column()

    price: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=10,scale=2),
        nullable=True,
        )

    bio: Mapped[str | None] = mapped_column(
            nullable=True,
            )

    # Foreign key for User:
    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            )

    user_profile = relationship("User", back_populates="practitioner_profile")

    # Foreign key for Availability:
    own_availabilities = relationship("Availability", back_populates="practitioner_profile")


