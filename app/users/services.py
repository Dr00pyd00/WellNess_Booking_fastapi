from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, or_

from app.core.exceptions import item_already_exist_field_error_msg, item_not_found_error_msg
from app.core.models_mixins.mixin_status import StatusEnum
from app.core.security.pw_hashing import hash_pw, verify_pw
from app.users.exceptions import non_admin_user_try_delete_other_user_error_msg, try_soft_delete_last_admin_error_msg, user_already_soft_deleted_error_msg, user_try_patch_other_user_error_msg, user_try_update_pw_but_old_wrong_error_msg
from app.users.models import User, UserRoleEnum
from app.users.schemas import UserCreationFormSchema, UserUpdatePasswordFormSchema, UserUpdateProfileFormSchema


# Functions =========================================================================================================== #
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

async def get_user_by_username_or_404(user_username: str, db: AsyncSession)->User:
    """try find user, if not found raise HTTPException 404 NOT FOUND

    Args:
        user_username(str): user username to find
        db (AsyncSession): database session

    Raises:
        HTTPException: 404 NOT FOUND

    Returns:
        User: User object
    """

    result = await db.execute(select(User).where(User.username == user_username ))
    user = result.scalar_one_or_none()

    if not user:
        item_not_found_error_msg(item_name="User")

    return user



async def get_user_by_email_or_404(user_email: str, db: AsyncSession)->User:
    """try find user, if not found raise HTTPException 404 NOT FOUND

    Args:
        user_email(str): user email to find
        db (AsyncSession): database session

    Raises:
        HTTPException: 404 NOT FOUND

    Returns:
        User: User object
    """

    result = await db.execute(select(User).where(User.email == user_email))
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



# GET ONE USER BY ID:
async def get_user_by_id_service(
        user_id:int, 
        db: AsyncSession
)->User:
    """find one user by ID or raise HTTPException

    Args:
        user_id (int): ID of user you want to find
        db (AsyncSession): databse session async

    Returns:
        User: User object.
    """

    user = await get_user_by_id_or_404(user_id=user_id, db=db)

    return user


# ==================== POST ==============================#

# CREATE USER:

async def create_user_service(
        user_data: UserCreationFormSchema,
        db: AsyncSession
)->User:
    
    # # unique username:
    # result = await db.execute(select(User).where(User.username ==user_data.username))
    # existing_user = result.scalar_one_or_none() # equivalent de "first()"
    # if existing_user:
    #     item_already_exist_field_error_msg("User", "username")
    
    # # unique email if email not none:
    # result2 = await db.execute(select(User).where(User.email == user_data.email))
    # existing_user_2 = result2.scalar_one_or_none()
    # if existing_user_2:
    #     item_already_exist_field_error_msg("User", "email")

    # 2 en 1 pro:
    conditions = [User.username ==user_data.username]
    if user_data.email is not None:
        conditions.append(User.email ==user_data.email)
    result = await db.execute(select(User).where(or_(*conditions)))
    existing_user = result.scalar_one_or_none()

    # gestion errreurs:
    if existing_user:
        if existing_user.username == user_data.username:
            item_already_exist_field_error_msg("User", "username")
        if existing_user.email == user_data.email:
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

# UPDATE PROFILE : NOT PASSWORD
async def update_user_profile_service(
        current_user: User,
        new_user_data: UserUpdateProfileFormSchema,
        db: AsyncSession
)->User:
    
    user = await get_user_by_id_or_404(user_id=current_user.id, db=db)

    new_user_data_dict = new_user_data.model_dump(exclude_none=True)
    for k,v in new_user_data_dict.items():
        setattr(user,k,v)

    await db.commit()
    await db.refresh(user)

    return user

# UPDATE PROFILE PASSWORD ONLY WITH VERIF
async def update_user_password_service(
        current_user: User,
        new_user_pw_data: UserUpdatePasswordFormSchema,
        db: AsyncSession
)->User:
    
    user = await get_user_by_id_or_404(user_id=current_user.id, db=db)

    # check old pw :
    old_pw_good = verify_pw(new_user_pw_data.old_password, user.password)
    if not old_pw_good:
        user_try_update_pw_but_old_wrong_error_msg(user_id=user.id)
    
    new_pw = hash_pw(new_user_pw_data.new_password)
    setattr(user,"password", new_pw)

    await db.commit()
    await db.refresh(user)

    return user
 




# ==================== DELETE ============================#

# Delete user 
async def soft_delete_user_service(
        current_user: User,
        user_id: int, # user id to delete
        db: AsyncSession,
)->User:
    """soft delete a user: 
    - user can't delete other user account
    - ADMIN can delete other user account
    - ADMIN cant delete the last admin account


    Args:
        current_user (User): current user 
        user_id (int): id of user who want to soft-delete

    Returns:
        User: soft deleted user refreshed
    """

    user_to_soft_deleted = await get_user_by_id_or_404(user_id=user_id, db=db)

    # if already soft-deleted:
    if user_to_soft_deleted.deleted_at is not None:
        user_already_soft_deleted_error_msg(user_id=user_to_soft_deleted.id)

    # protect last admin acc:
    res = await db.execute(select(func.count(User.id)).where(User.deleted_at == None, User.role == UserRoleEnum.ADMIN))
    admin_count = res.scalar()

    if user_to_soft_deleted.role == UserRoleEnum.ADMIN and admin_count == 1:
        try_soft_delete_last_admin_error_msg()

    # non-admin can delete only his acc:
    if current_user.role != UserRoleEnum.ADMIN and user_id != current_user.id:
        non_admin_user_try_delete_other_user_error_msg()

    user_to_soft_deleted.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user_to_soft_deleted)

    return user_to_soft_deleted

    

    





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








