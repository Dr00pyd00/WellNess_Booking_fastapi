

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base
from app.core.models_mixins.mixin_soft_delete import SoftDeleteMixin
from app.core.models_mixins.mixin_status import StatusMixin
from app.core.models_mixins.mixin_timestamp import TimeStampMixin


class Booking(TimeStampMixin, StatusMixin, SoftDeleteMixin, Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    message_to_practitioner: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )

    # Foreigns keys:

    # user 
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        )
   
    user_profile = relationship("User", back_populates="owner_bookings")

    # availability 
    availability_id: Mapped[int] = mapped_column(
        ForeignKey("availabilities.id", ondelete="CASCADE"),
        )

    availability = relationship("Availability", back_populates="current_booking")

