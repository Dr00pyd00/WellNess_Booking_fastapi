from typing import Annotated, List

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.users.schemas import UserCreationFormSchema, UserDataFromDbSchema, UserFilterRoleStatusDeletedSchema
from app.users.services import create_user_service, get_all_users_service
from app.users.users_filter import get_user_filters_role_status_softdeleted


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




# ----------------------------------- # 
# --------- ALL --------------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# SEE ALL USER (filters in query)
@router.get(
        "/all_list", 
        status_code=status.HTTP_200_OK, 
        response_model=List[UserDataFromDbSchema]
        )
async def get_all_users(
    
    db: Annotated[AsyncSession, Depends(get_db)],
    users_filters: Annotated[UserFilterRoleStatusDeletedSchema, Depends(get_user_filters_role_status_softdeleted)],
    skip: Annotated[int, Query(ge=0, description="number of users to skip.")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="number of users in a request: 1 to 100 max.")] = 10,
)->List[UserDataFromDbSchema]:
    
    return await get_all_users_service(
        db=db,
        skip=skip,
        limit=limit,
        users_filters=users_filters
    )

# ==================== POST ==============================#

# CREATE USER 
@router.post(
        path="/",
        status_code=status.HTTP_201_CREATED,
        response_model=UserDataFromDbSchema
        )
async def create_user(
    user_form_data_fields: UserCreationFormSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
)->UserDataFromDbSchema:

    return await create_user_service(user_data=user_form_data_fields, db=db)


# ==================== PUT ===============================#

# ==================== PATCH =============================#

# ==================== DELETE ============================#



# ----------------------------------- # 
# --------- ADMIN ONLY -------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

# ==================== PUT ===============================#

# ==================== PATCH =============================#

# ==================== DELETE ============================#


# ----------------------------------- # 
# --------- PRACTITIONER ONLY ------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

# ==================== PUT ===============================#

# ==================== PATCH =============================#

# ==================== DELETE ============================#





