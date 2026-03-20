from calendar import c
from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.jwt import get_current_user
from app.users.schemas import UserCreationFormSchema, UserDataFromDbSchema, UserFilterRoleStatusDeletedSchema, UserUpdatePasswordFormSchema, UserUpdateProfileFormSchema
from app.users.services import create_user_service, delete_current_user_service, get_all_users_service, update_user_password_service, update_user_profile_service
from app.users.users_filter import get_user_filters_role_status_softdeleted
from app.users.models import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




# ----------------------------------- # 
# --------- ALL --------------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ME : the current user
@router.get(
        "/me", 
        status_code=status.HTTP_200_OK, 
        response_model=UserDataFromDbSchema
            )
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
)->UserDataFromDbSchema:
    
    return current_user

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

# UPDATE PROFILE : NOT THE PASSWORD:
@router.patch(
        "/update_profile",
        status_code=status.HTTP_200_OK ,
        response_model=UserDataFromDbSchema,
        )
async def update_user_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    new_profile_data: Annotated[UserUpdateProfileFormSchema, Body(...,description="Fields data for update user profile.")] = None,
)->UserDataFromDbSchema:
    
    return await update_user_profile_service(
        current_user=current_user,
        new_user_data=new_profile_data,
        db=db
    )

# UPDATE CHANGE PASSWORD WITH VERIF:
@router.patch(
        "/update_password",
        status_code=status.HTTP_200_OK,
        response_model=UserDataFromDbSchema,
)
async def update_user_password(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    new_and_old_pw_data: Annotated[UserUpdatePasswordFormSchema, Body(..., description="old pw for check, and new pw for replace.")]
)->UserDataFromDbSchema:
    
    return await update_user_password_service(
        current_user=current_user,
        new_user_pw_data=new_and_old_pw_data,
        db=db
    )

# ==================== DELETE ============================#

# SOFT DELETE CURRENT USER
@router.delete(
        "/me", 
        status_code=status.HTTP_200_OK,
        response_model=UserDataFromDbSchema,
               )
async def delete_user_by_id_service(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
)->UserDataFromDbSchema:
    
    return await delete_current_user_service(
        current_user=current_user,
        db=db,
    )



# ----------------------------------- # 
# --------- ADMIN ONLY -------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

# ==================== PUT ===============================#

# ==================== PATCH =============================#

# ==================== DELETE ============================#


   # user_id: Annotated[int, Query(..., description="ID of user who want to delete.")],
# ----------------------------------- # 
# --------- PRACTITIONER ONLY ------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

# ==================== PUT ===============================#

# ==================== PATCH =============================#

# ==================== DELETE ============================#





