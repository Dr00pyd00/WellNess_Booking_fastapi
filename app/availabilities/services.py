
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.models_mixins.mixin_status import StatusEnum
from app.practitioners.models import Practitioner
from app.users.models import User
from app.availabilities.exceptions import (
    avail_already_soft_deleted_error_msg, 
    pract_try_soft_delete_inexistant_avail_slot_error_msg, 
    pract_try_soft_delete_not_own_avail_error_msg, 
    try_find_avail_but_deleted_error_msg, 
    try_find_avail_but_inactive_error_msg, 
    try_find_avail_but_inexistant_error_msg, 
    user_try_to_create_avail_when_not_the_practitioner_error_msg,
)
from app.availabilities.models import Availability
from app.availabilities.schemas import AvailabilityCreationFormSchema
from app.practitioners.services import get_practitioner_by_id_or_404





# ================================================================ #
#  HELPERS — fonctions internes, non exposées au router            #
# ================================================================ #

async def get_availability_by_id_or_404(avail_id:int, db:AsyncSession)->Availability:
    result = await db.execute(
        select(Availability)
        .where(Availability.id == avail_id)
        # .where(Availability.active_only())
        # .where(Availability.not_deleted_only())
        )
    avail:Availability | None = result.scalar_one_or_none()
    if avail is None:
        try_find_avail_but_inexistant_error_msg()
    if avail.deleted_at is not None:
        try_find_avail_but_deleted_error_msg()
    if avail.status != StatusEnum.ACTIVE:
        try_find_avail_but_inactive_error_msg()
    return avail


async def get_all_free_avail_of_a_practitioner_or_none(pract_id:int, db:AsyncSession)->List[Availability] | None:
    pract = await get_practitioner_by_id_or_404(practitioner_id=pract_id, db=db)
    
    result = await db.execute(
        select(Availability)
        .where(Availability.practitioner_id == pract_id)
        .where(Availability.is_booked == False)
    )
    avail_list = result.scalars().all()
    if len(avail_list) < 1:
        return None
    return avail_list




# ================================================================ #
#  USER — services accessibles à tout utilisateur connecté         #
# ================================================================ #

async def get_all_avail_of_a_practitioner_service(
        pract_id:int,
        db:AsyncSession
)->List[Availability] :
    await get_practitioner_by_id_or_404(practitioner_id=pract_id,db=db)

    result = await db.execute(
        select(Availability)
        .where(Availability.practitioner_id == pract_id)
        .where(Availability.not_deleted_only())
        .where(Availability.active_only())

    )
    avail_list = result.scalars().all()
    return avail_list

# ================================================================ #
#  PRACTITIONER — services accessibles pour les practitioners      #
# ================================================================ #

async def create_avail_slot_service(
        current_user:User,
        avail_slot_data:AvailabilityCreationFormSchema,
        db:AsyncSession
)->Availability:

    result = await db.execute(
        select(Practitioner)
        .where(Practitioner.user_id == current_user.id)
    )
    pract = result.scalar_one_or_none()
    if pract is None:
        user_try_to_create_avail_when_not_the_practitioner_error_msg()

    new_slot = Availability(**avail_slot_data.model_dump(),practitioner_id=pract.id)
    db.add(new_slot)
    await db.commit()
    await db.refresh(new_slot)
    return new_slot


async def soft_delete_avail_slot_service(
        current_user:User,
        slot_id:int, 
        db:AsyncSession,
)->Availability:
    result = await db.execute(
        select(Availability)
        .where(Availability.id == slot_id)
        .options(selectinload(Availability.practitioner_profile))
        )
    slot_to_delete = result.scalar_one_or_none()
    if slot_to_delete is None:
        pract_try_soft_delete_inexistant_avail_slot_error_msg()
    if slot_to_delete.practitioner_profile.user_id != current_user.id:
        pract_try_soft_delete_not_own_avail_error_msg()
    if slot_to_delete.deleted_at is not None:
        avail_already_soff_deleted_error_msg()
    
    slot_to_delete.soft_delete()
    await db.commit()
    await db.refresh(slot_to_delete)
    return slot_to_delete
    


