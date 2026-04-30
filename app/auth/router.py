
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import login_service
from app.core.security.schemas import BearerTokenSchema
from app.dependencies.database import get_db





router = APIRouter(
    tags=["Authentication"]
)





# ----------------------------------- # 
# --------- ALL --------------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=BearerTokenSchema,
             )
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
)->Any:
    
    return await login_service(user_credentials=user_credentials, db=db)



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







