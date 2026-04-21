from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.dependencies.database import get_db
from app.dependencies.jwt import get_current_user
from app.practitioners.practitioners_filters import get_practitioner_speciality_status_softdeleted
from app.practitioners.schemas import (
        PractitionerCreationFormSchema,
        PractitionerDataForPatientsSchema, 
        PractitionerDataFromDbSchema, 
        PractitionerFilterSpecialityStatusDeletedSchema,
        PractitionerUpdateFormSchema,
        )
from app.practitioners.services import (
        create_practitioner_profile_service,
        get_all_practitioners_service,
        get_practitioner_by_id_service,
        update_practitioner_profile_service,

        )


router = APIRouter(
    prefix="/practitioner",
    tags=["Practitioner"]
)

# ================================================================ #
#  USER — routes accessibles à tout utilisateur connecté           #
# ================================================================ #

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[PractitionerDataForPatientsSchema]
)
async def get_all_practitioners(
    db: Annotated[AsyncSession, Depends(get_db)],
    practitioner_filters: Annotated[PractitionerFilterSpecialityStatusDeletedSchema, Depends(get_practitioner_speciality_status_softdeleted)],
    skip: Annotated[int, Query(ge=0, description="number of practitioners to skip.")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="number of practitioners in a request: 1 to 100 max.")] = 10,

)-> List[PractitionerDataForPatientsSchema]:
    
    return await get_all_practitioners_service(
        db=db,
        limit=limit,
        skip=skip,
        practitioner_filters=practitioner_filters
    )


@router.get(
    "/{pract_id}/profile",
    status_code=status.HTTP_200_OK,
    response_model=PractitionerDataForPatientsSchema,
        )
async def get_practitioner_detail(
    db: Annotated[AsyncSession, Depends(get_db)],
    pract_id: Annotated[int, Path(..., description="ID of practitioner detail you want to see.")],
    )->PractitionerDataForPatientsSchema:

    return await get_practitioner_by_id_service(pract_id=pract_id, db=db)
    


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PractitionerDataFromDbSchema,
)
async def create_practitioner_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    practitioner_data: Annotated[PractitionerCreationFormSchema, Body(description="Fields for new profile practitioner page.")],
)->PractitionerDataFromDbSchema:
    
    return await create_practitioner_profile_service(
        user_id=current_user.id,
        practitioner_data=practitioner_data,
        db=db
    )


@router.patch(
        "/{pract_id}/update",
        status_code=status.HTTP_200_OK,
        response_model=PractitionerDataFromDbSchema
        )
async def update_practitioner_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    new_data: PractitionerUpdateFormSchema,
    pract_id: Annotated[int, Path(..., descritption="practitioner ID you want to update profile.")],
    )->PractitionerDataFromDbSchema:

    return await update_practitioner_profile_service(
            current_user_id=current_user.id,
            pract_id=pract_id,
            db=db,
            new_data=new_data,
            )















