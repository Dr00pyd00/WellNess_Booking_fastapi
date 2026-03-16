from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Numeric,
    String,
    Enum as sqlEnum,
    func,
    text,
    ForeignKey,
    
)
from sqlalchemy.orm import relationship

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

    id = Column(
        Integer,
        primary_key=True,
    )

    speciality = Column(
        sqlEnum(PractitionerSpecialtyEnum, name="practitioner_speciality_enum"),
        nullable=False,
    )

    # consult a distance
    is_remote_possible = Column(
        Boolean,
        nullable=False,
        server_default=text("FALSE"),
        default=False,
    )

    address = Column(
        String,
        nullable=False
    )

    price = Column(
        # precision => 10 chiffre au total
        # scale => 2 chiffre apres virgule
        Numeric(precision=10,scale=2),
        nullable=True, # non renseigner ?
    )

    bio = Column(
        String,
        nullable=True,
    )   

    # Foreign key for User:
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # force one to one 
    )

    user_profile = relationship("User", back_populates="practitioner_profile")

    # Foreign key for Availability:
    own_availabilities = relationship("Availability", back_populates="practitioner_profile")
