from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.schemas import PatientBookingDataForPractitionerSchema, TakeBookingByPatientFormSchema
from app.bookings.services import user_take_booking_service
from app.dependencies.database import get_db
from app.dependencies.jwt import get_current_user
from app.users.models import User


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

# ================================================================ #
#  USER — services accessibles à tout utilisateur connecté         #
# ================================================================ #

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PatientBookingDataForPractitionerSchema,
)
async def user_take_availability(
    current_user: Annotated[User, Depends(get_current_user)],
    booking_data: TakeBookingByPatientFormSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
)->PatientBookingDataForPractitionerSchema:
    
    return  await user_take_booking_service(
        current_user=current_user,
        booking_data=booking_data,
        db=db,
    )
