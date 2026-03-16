from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Time,
    text,
    Enum as sqlEnum,

)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models_mixins.mixin_soft_delete import SoftDeleteMixin
from app.core.models_mixins.mixin_status import StatusMixin
from app.core.models_mixins.mixin_timestamp import TimeStampMixin



class DaysEnum(PyEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

# une instance est UN crenaux horaire.
class Availability(TimeStampMixin, StatusMixin, SoftDeleteMixin, Base):

    __tablename__ = "availabilities"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # ====== planning ========
    day = Column(
        sqlEnum(DaysEnum, name="days_enum"), 
        nullable=False,
    )

    start_time = Column(
        Time,
        nullable=False
    )


    end_time = Column(
        Time,
        nullable=False
    )
    # =======================

    is_booked = Column(
        Boolean,
        nullable=False,
        server_default=text("FALSE"),
        default=False,
    )


    # foreign keys
    
    # Practitioner:
    practitioner_id = Column(
        Integer,
        ForeignKey("practitioners.id", ondelete="CASCADE"),
        nullable=False,
    )
    practitioner_profile = relationship("Practitioner", back_populates="own_availabilities")

    # booking:
    current_booking = relationship("Booking", back_populates="availability", uselist=False)

