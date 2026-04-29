from datetime import date as date_t, time

from enum import Enum as PyEnum


from sqlalchemy import (
    Boolean,
    ForeignKey,
    Time,
    text,
    Date,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

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

    id: Mapped[int] = mapped_column(
            primary_key=True,
            )


    # ====== planning ========
    # day = Column(
    #     sqlEnum(DaysEnum, name="days_enum"), 
    #     nullable=False,
    # )

    date: Mapped[date_t] = mapped_column(
            Date,
            )

    start_time: Mapped[time] = mapped_column(
            Time,
            )

    end_time: Mapped[time] = mapped_column(
            Time,
            )
    # =======================

    is_booked: Mapped[bool] = mapped_column(
            Boolean,
            nullable=False,
            server_default=text("FALSE"),
            default=False,
            )
            

    # foreign keys
    
    # Practitioner:
    practitioner_id: Mapped[int] = mapped_column(
            ForeignKey("practitioners.id", ondelete="CASCADE"),
            )
            
    practitioner_profile = relationship("Practitioner", back_populates="own_availabilities")

    # booking:
    current_booking = relationship("Booking", back_populates="availability", uselist=False)

