from typing import Annotated

from fastapi import Query

from app.core.models_mixins.mixin_status import StatusEnum
from app.users.models import UserRoleEnum
from app.users.schemas import UserFilterRoleStatusDeletedSchema


def get_user_filters_role_status_softdeleted(
        role: Annotated[UserRoleEnum | None, Query(description="query for filter <role>.")] = None,
        status: Annotated[StatusEnum | None, Query(description="query for filter <status>")] = None,
        see_deleted: Annotated[bool, Query(description="query for filter soft deleted users, True=see them")] = False,
)->UserFilterRoleStatusDeletedSchema:
    
    return UserFilterRoleStatusDeletedSchema(
        role=role,
        status=status,
        see_deleted=see_deleted
    )

