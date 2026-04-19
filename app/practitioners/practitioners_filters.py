from typing import Annotated 

from fastapi import Query

from app.core.models_mixins.mixin_status import StatusEnum
from app.users.models import UserRoleEnum
from app.practitioners.models import PractitionerSpecialtyEnum

from app.practitioners.schemas import PractitionerFilterSpecialityStatusDeletedSchema



def get_practitioner_speciality_status_softdeleted(
        speciality: Annotated[PractitionerSpecialtyEnum | None, Query(description="query for filter <speciality>")] = None,
        status: Annotated[StatusEnum | None, Query(description="query for filter <status>")] = None,
        see_deleted: Annotated[bool, Query(description="query for filter soft deleted practitioners, True= see them.")] = False,
)-> PractitionerFilterSpecialityStatusDeletedSchema:
    return PractitionerFilterSpecialityStatusDeletedSchema(
        speciality=speciality,
        status=status,
        see_deleted=see_deleted
    )