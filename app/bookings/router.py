
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Path, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.booking_filters import get_booking_filters_status_deleted_bypatient_by_practitioner
from app.bookings.schemas import (
        BookingFilterStatusDeletedBookedPractPatientSchema, 
        PatientBookingDataForPractitionerSchema,
        TakeBookingByPatientFormSchema,
        )
from app.bookings.services import (
        admin_booking_list_service, 
        user_booking_list_service, 
        user_delete_booking_service, 
        user_take_booking_service,
        )
from app.dependencies.database import get_db
from app.dependencies.jwt import get_current_user, required_roles
from app.users.models import User, UserRoleEnum


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
async def user_take_booking(
    current_user: Annotated[User, Depends(get_current_user)],
    booking_data: TakeBookingByPatientFormSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
)->Any:
    
    return  await user_take_booking_service(
        current_user=current_user,
        booking_data=booking_data,
        db=db,
    )


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatientBookingDataForPractitionerSchema,
)
async def user_delete_booking(
    current_user: Annotated[User, Depends(get_current_user)],
    booking_id: Annotated[int, Path(..., description="Booking ID you wantto delete.")],
    db: Annotated[AsyncSession, Depends(get_db)],
)->Any:
    
    return await user_delete_booking_service(
        current_user=current_user,
        booking_id=booking_id,
        db=db
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[PatientBookingDataForPractitionerSchema],
)
async def user_get_all_own_booking(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
)->Any:
    
    return await user_booking_list_service(
        current_user=current_user,
        db=db
    )



# ================================================================ #
#  ADMIN — services réservés aux admins                            #
# ================================================================ #

@router.get(
    "/admin",
    status_code=status.HTTP_200_OK,
    response_model=List[PatientBookingDataForPractitionerSchema]
)
async def admin_get_all_booking(
current_user: Annotated[User, Depends(required_roles(UserRoleEnum.ADMIN))], 
    db: Annotated[AsyncSession, Depends(get_db)],
    filters: Annotated[BookingFilterStatusDeletedBookedPractPatientSchema, 
                       Depends(get_booking_filters_status_deleted_bypatient_by_practitioner)],
    skip: Annotated[int, Query(ge=0, description="number of booking to skip.")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="number of booking in a request: 1 to 100 max.")] = 10,
)->Any:
    
    return await  admin_booking_list_service(
        limit=limit,
        skip=skip,
        filters=filters,
        db=db
    )



