from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.availabilities.schemas import AvailabilityCreationFormSchema, AvailabilityFullReservationViewSchema, AvailabilityUserReservationViewSchema
from app.availabilities.services import create_avail_slot_service, get_all_avail_of_a_practitioner_service, soft_delete_avail_slot_service
from app.dependencies.database import get_db
from app.dependencies.jwt import required_roles
from app.users.models import User, UserRoleEnum




router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)



# ================================================================ #
#  PRACTITIONER — services accessibles pour les practitioners      #
# ================================================================ #

@router.get(
    "/{pract_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[AvailabilityFullReservationViewSchema]
)
async def get_all_availabilities(
    pract_id: Annotated[int, Path(..., description="Practitioner ID that you want check availabilities.")],
    db: Annotated[AsyncSession, Depends(get_db)]
)->List[AvailabilityFullReservationViewSchema]:
    
    return await get_all_avail_of_a_practitioner_service(
        pract_id=pract_id,
        db=db
    )
    

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AvailabilityUserReservationViewSchema,
)
async def create_availability_slot(
    current_user: Annotated[User, Depends(required_roles(UserRoleEnum.PRACTITIONER))],
    slot_data: AvailabilityCreationFormSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
)->AvailabilityUserReservationViewSchema:
    
    return await create_avail_slot_service(
        current_user=current_user,
        avail_slot_data=slot_data,
        db=db
    )


@router.delete(
    "/{avail_id}",
    status_code=status.HTTP_200_OK,
    response_model=AvailabilityFullReservationViewSchema,
)
async def soft_delete_avail_slot(
    current_user: Annotated[User, Depends(required_roles(UserRoleEnum.PRACTITIONER))],
    avail_id: Annotated[int, Path(..., description="availability ID you want to soft_delete.")],
    db: Annotated[AsyncSession, Depends(get_db)],
)->AvailabilityFullReservationViewSchema:
    
    return await soft_delete_avail_slot_service(
        current_user=current_user,
        slot_id=avail_id,
        db=db
    )