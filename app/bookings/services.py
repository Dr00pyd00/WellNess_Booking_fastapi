
from datetime import date
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.availabilities.models import Availability
from app.availabilities.services import get_availability_by_id_or_404
from app.bookings.exceptions import (
        user_try_delete_booking_not_owner_error_msg, 
        user_try_take_already_booked_slot_error_msg, 
        user_try_take_slot_in_past_error_msg,
        )
from app.bookings.models import Booking
from app.bookings.schemas import BookingFilterStatusDeletedBookedPractPatientSchema, TakeBookingByPatientFormSchema
from app.core.exceptions import item_not_found_error_msg
from app.users.models import User



# ================================================================ #
#  HELPERS — fonctions internes, non exposées au router            #
# ================================================================ #

async def get_booking_by_id_or_404(booking_id:int, db:AsyncSession)->Booking:
    result = await db.execute(
        select(Booking)
        .where(Booking.id == booking_id)
        )
    booking = result.scalar_one_or_none()
    if booking is None:
        item_not_found_error_msg(item_name="booking")
    return booking


async def get_active_booking_by_id_or_404(booking_id:int, db:AsyncSession)->Booking:
    result = await db.execute(
        select(Booking)
        .where(Booking.id == booking_id)
        .where(Booking.active_only())
        .where(Booking.not_deleted_only())
    )
    booking = result.scalar_one_or_none()
    if booking is None:
        item_not_found_error_msg(item_name="booking")
    return booking




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


async def user_delete_booking_service(
        current_user:User,
        db:AsyncSession,
        booking_id:int
)->Booking:
    booking:Booking = await get_active_booking_by_id_or_404(booking_id=booking_id,db=db)
    if booking.user_id != current_user.id:
       user_try_delete_booking_not_owner_error_msg()
    avail:Availability = await get_availability_by_id_or_404(avail_id=booking.availability_id, db=db)
    avail.is_booked = False 
    booking.soft_delete()
    await db.commit()
    await db.refresh(booking, ["user_profile","availability"])
    await db.refresh(avail)
    return booking


async def user_booking_list_service(
        current_user:User,
        db:AsyncSession,
)->Sequence[Booking]:
    
    result = await db.execute(
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .where(Booking.active_only())
        .options(
            selectinload(Booking.availability),
            selectinload(Booking.user_profile)
        )
    )
    booking_list = result.scalars().all()
    return booking_list




# ================================================================ #
#  PRACTITIONER — services accessibles pour les practitioners      #
# ================================================================ #



# ================================================================ #
#  ADMIN — services réservés aux admins                            #
# ================================================================ #

async def admin_booking_list_service(
        limit:int,
        skip:int,
        filters: BookingFilterStatusDeletedBookedPractPatientSchema,
        db:AsyncSession
)->Sequence[Booking]:
    
    query = (
        select(Booking)
        .offset(skip)
        .limit(limit)
        .options(           # pour charger
            selectinload(Booking.availability)
        )
        .join(Booking.availability)    # pour filtrer
    )

    if filters.status:
        query = query.where(Booking.status.in_(filters.status))
    if filters.see_deleted is False:
        query = query.where(Booking.deleted_at == None)
    if filters.by_practitioner:
        query = query.where(Availability.practitioner_id == filters.by_practitioner) 
    if filters.by_patient:
        query = query.where(Booking.user_id == filters.by_patient)

    result = await db.execute(query)
    booking_list = result.scalars().all()
    return booking_list
        
    


    

    




