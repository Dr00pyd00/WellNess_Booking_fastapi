from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.users.schemas import UserCreationFormSchema, UserDataFromDbSchema
from app.users.services import create_user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




# ----------------------------------- # 
# --------- ALL --------------------- #
# ----------------------------------- #

# ==================== GET ===============================#

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





