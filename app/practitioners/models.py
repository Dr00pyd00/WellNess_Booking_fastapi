from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
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

    adresse = Column(
        String,
        nullable=False
    )

    price = Column(
        String,
        nullable=True, # non renseigner ?
    )

    bio = Column(
        String,
        nullable=True,
    )   

    # Foreign key:
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # force one to one 
    )

    user_profile = relationship("User", back_populates="practitioner_profile")


