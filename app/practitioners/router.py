from typing import Annotated, List

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.practitioners.practitioners_filters import get_practitioner_speciality_status_softdeleted
from app.practitioners.schemas import PractitionerDataForPatientsSchema, PractitionerFilterSpecialityStatusDeletedSchema
from app.practitioners.services import get_all_practitioners_service


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