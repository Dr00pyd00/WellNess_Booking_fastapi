from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.availabilities.models import Availability
from app.availabilities.services import get_availability_by_id_or_404
from app.bookings.exceptions import user_try_take_already_booked_slot_error_msg, user_try_take_slot_in_past_error_msg
from app.bookings.models import Booking
from app.bookings.schemas import TakeBookingByPatientFormSchema
from app.users.models import User



# ================================================================ #
#  HELPERS — fonctions internes, non exposées au router            #
# ================================================================ #




# ================================================================ #
#  USER — services accessibles à tout utilisateur connecté         #
# ================================================================ #



async def user_take_booking_service(
        current_user:User,
        db:AsyncSession,
        booking_data: TakeBookingByPatientFormSchema, # contain avail_id and message.
)->Booking:
    avail: Availability = await get_availability_by_id_or_404(avail_id=booking_data.availability_id, db=db)
    # check if avail is valid
    if avail.is_booked is True:
        user_try_take_already_booked_slot_error_msg()
    if avail.date < date.today():
        user_try_take_slot_in_past_error_msg()
    
    booking = Booking(**booking_data.model_dump(),user_id=current_user.id)
    avail.is_booked = True
    db.add(booking)
    await db.commit()
    await db.refresh(booking, ["user_profile", "availability"])
    return booking

    

    





# ================================================================ #
#  PRACTITIONER — services accessibles pour les practitioners      #
# ================================================================ #