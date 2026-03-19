


# booking = reservation 
# prend un availability , un user 


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models_mixins.mixin_soft_delete import SoftDeleteMixin
from app.core.models_mixins.mixin_status import StatusMixin
from app.core.models_mixins.mixin_timestamp import TimeStampMixin


class Booking(TimeStampMixin, StatusMixin, SoftDeleteMixin, Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    message_to_practitioner = Column(
        String,
        nullable=True
    )

    # Foreigns keys:

    # user 
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_profile = relationship("User", back_populates="owner_bookings")

    # availability 
    availability_id = Column(
        Integer,
        ForeignKey("availabilities.id", ondelete="CASCADE"),
        nullable=False,
    )
    availability = relationship("Availability", back_populates="current_booking")

