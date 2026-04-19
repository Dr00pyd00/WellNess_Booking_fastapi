from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import item_not_found_error_msg

from app.practitioners.schemas import PractitionerCreationFormSchema, PractitionerDataFromDbSchema, PractitionerFilterSpecialityStatusDeletedSchema
from app.users.services import get_user_by_id_or_404
from app.users.models import User, UserRoleEnum
from app.practitioners.models import Practitioner
from app.practitioners.exceptions import (
    try_create_practitioner_profile_when_not_practitioner_error_msg,
    try_create_practitioner_profile_when_already_have_error_msg,
    )


# ================================================================ #
#  HELPERS — fonctions internes, non exposées au router            #
# ================================================================ #

async def get_practitioner_by_id_or_404(practitioner_id:int, db: AsyncSession)->Practitioner:
    """try find practitioner, if not exist raise HTTPException 404 NOT FOUND

    Args:
        practitioner_id (int): practitioner id to find

    Returns:
        User: practitioner object
        
    """

    result = await db.execute(select(Practitioner).where(Practitioner.id == practitioner_id))
    practitioner = result.scalar_one_or_none()
    if not practitioner:
        item_not_found_error_msg(item_name="practitioner")
    return practitioner
        


# ================================================================ #
#  USER — services accessibles à tout utilisateur connecté         #
# ================================================================ #



async def create_practitioner_profile_service(
    user_id: int,
    practitioner_data:  PractitionerCreationFormSchema,
    db: AsyncSession,
)->PractitionerDataFromDbSchema:
    user:User = await get_user_by_id_or_404(user_id=user_id, db=db)

    if user.role != UserRoleEnum.PRACTITIONER:
        try_create_practitioner_profile_when_not_practitioner_error_msg()
    elif user.practitioner_profile is not None:
        try_create_practitioner_profile_when_already_have_error_msg()

    new_profile = Practitioner(**practitioner_data.model_dump(), user_id=user_id)
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile



async def get_all_practitioners_service(
        db: AsyncSession,
        skip:int,
        limit:int,
        practitioner_filters: PractitionerFilterSpecialityStatusDeletedSchema 
)-> List[Practitioner]:
    
    query = select(Practitioner).offset(skip).limit(limit)

    # filters: 
    if practitioner_filters.speciality:
        query = query.where(Practitioner.speciality == practitioner_filters.speciality)
    if practitioner_filters.status:
        query = query.where(Practitioner.status == practitioner_filters.status)
    if practitioner_filters.see_deleted is False:
        query = query.where(Practitioner.deleted_at == None)

    result = await db.execute(query)
    practitioners_list = result.scalars().all()
    return practitioners_list

    
        
        