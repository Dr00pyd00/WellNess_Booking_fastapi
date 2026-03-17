from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import item_already_exist_field_error_msg, item_not_found_error_msg
from app.core.security.pw_hashing import hash_pw
from app.users.models import User
from app.users.schemas import UserCreationFormSchema


# Functions ==================== #
async def get_user_by_id_or_404(user_id:int, db: AsyncSession)->User:
    """try find user if not exist raise HTTPException 404 NOT FOUND
    Args:
        user_id (int): user id to find

    Returns:
        User: user object
        
    """

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        item_not_found_error_msg(item_name="User")
    
    return user



# ----------------------------------- # 
# --------- ALL --------------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# GET ALL USERS 
async def get_all_users_service(
        db: AsyncSession,
        skip: int,
        limit: int
)->List[User]:
    """get list of users 

    Args:
        db (AsyncSession): the db session
        skip (int): num of item to skip 
        limit (int): max item in a request

    Returns:
        List[User]: User list
    """

    # inclus pagination
    result = await db.execute(select(User).offset(skip).limit(limit))


    users_list = result.scalars().all()
    # scalars() : extrait les objets pythons 
    # all() : les mets dans une liste

    return users_list


# ==================== POST ==============================#

# CREATE USER:

async def create_user_service(
        user_data: UserCreationFormSchema,
        db: AsyncSession
)->User:
    
    # unique email:
    result = await db.execute(select(User).where(User.email ==user_data.email))
    existing_user = result.scalar_one_or_none() # equivalent de "first()"
    if existing_user:
        item_already_exist_field_error_msg("User", "email")

    # hash pw:
    user_data_dict = user_data.model_dump()
    user_data_dict["password"] = hash_pw(user_data_dict["password"])

    new_user = User(**user_data_dict)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

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








