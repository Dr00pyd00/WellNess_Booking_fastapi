from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, or_

from app.core.exceptions import item_already_exist_field_error_msg, item_not_found_error_msg
from app.core.models_mixins.mixin_status import StatusEnum
from app.core.security.pw_hashing import hash_pw, verify_pw
from app.users.exceptions import admin_cant_change_status_or_role_for_other_admin_error_msg, admin_cant_self_change_role_error_msg, admin_cant_self_change_status_error_msg, non_admin_user_try_delete_other_user_error_msg, try_soft_delete_last_admin_error_msg, user_already_soft_deleted_error_msg, user_is_not_soft_deleted, user_try_patch_other_user_error_msg, user_try_update_pw_but_old_wrong_error_msg
from app.users.models import User, UserRoleEnum
from app.users.schemas import UserCreationFormSchema, UserFilterRoleStatusDeletedSchema, UserUpdatePasswordFormSchema, UserUpdateProfileFormSchema


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
        limit: int,
        users_filters: UserFilterRoleStatusDeletedSchema
)->List[User]:
    """get list of users 

    Args:
        db (AsyncSession): the db session
        skip (int): num of item to skip 
        limit (int): max item in a request

    Returns:
        List[User]: User list
    """

    # base:
    # inclure pagination
    query = select(User).offset(skip).limit(limit)


    # inclure filters
    if users_filters.role:
        query = query.where(User.role == users_filters.role)
    if users_filters.status:
        query = query.where(User.status == users_filters.status)
    if users_filters.see_deleted is False:
        query = query.where(User.deleted_at == None)

    result =  await db.execute(query)


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
    """create a new user 

    Args:
        user_data (UserCreationFormSchema):  data for new user creation
        db (AsyncSession): databse (async)

    Returns:
        User: user created
    """
    
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
    """update a user profile

    Args:
        current_user (User): current user
        new_user_data (UserUpdateProfileFormSchema): form with all new data for update
        db (AsyncSession): database (async)

    Returns:
        User: updated user
    """
    
    user = await get_user_by_id_or_404(user_id=current_user.id, db=db)

    if new_user_data:

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
   
# delete current_user account
async def delete_current_user_service(
        current_user: User,
        db: AsyncSession,
)->User:
    """take current user and delete it.

    Args:
        current_user (User): current user want want to delete.
        db (AsyncSession): database (async)

    Returns:
        User: updated user soft deleted.
    """
    
    user_to_delete = await get_user_by_id_or_404(user_id=current_user.id, db=db)

    # protect last admin:
    res = await db.execute(select(func.count(User.id)).where(User.deleted_at == None, User.role == UserRoleEnum.ADMIN))
    admin_count = res.scalar()
    if user_to_delete.role == UserRoleEnum.ADMIN and admin_count == 1:
        try_soft_delete_last_admin_error_msg()
    

    user_to_delete.soft_delete()
    await db.commit()
    await db.refresh(user_to_delete)
    return user_to_delete



# ----------------------------------- # 
# --------- ADMIN ONLY -------------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

# ==================== PUT ===============================#

# ==================== PATCH =============================#


# RESTTORE A SOFT DELETED USER AS ADMIN
async def restore_user_soft_deleted_as_admin_service(
        current_user: User,
        user_id: int, # user id to restore
        db: AsyncSession,
)->User:
    """take user ID and restore of softdelted

    Args:
        current_user (User): the admin user
        user_id (int): user ID you want to restore
        db (AsyncSession): database (async)

    Returns:
        User:  restored user data
    """
    user_to_restore = await get_user_by_id_or_404(user_id=user_id, db=db)

    if user_to_restore is None:
        item_not_found_error_msg(item_name="user")

    if user_to_restore.deleted_at is None:
        user_is_not_soft_deleted()

    if current_user.id == user_id:
        pass 
        # fill if you want forbid admin to cant restore his own account

    if user_to_restore.role == UserRoleEnum.ADMIN:
        pass
        # fill if you want restrict admin for admins.

    user_to_restore.restore_from_soft_delete()
    await db.commit()
    await db.refresh(user_to_restore)

    return user_to_restore


    

    




# SWAP STATUS by ADMIN:
async def swap_user_status_by_admin_service(
        admin_id: int,
        user_to_swap_id: int,
        new_status: StatusEnum,
        db: AsyncSession,
)->User:
    """change user status as admin

    Args:
        admin_id (int): the current_user ADMIN ID
        user_to_swap_id (int): user you want to swap ID
        new_status (StatusEnum): status you want to setup
        db (AsyncSession): databse (async)

    Returns:
        User: updated user with new status.
    """
    
    
    if admin_id == user_to_swap_id:
        admin_cant_self_change_status_error_msg()
    
    user = await get_user_by_id_or_404(user_id=user_to_swap_id, db=db)

    if user.role == UserRoleEnum.ADMIN:
        admin_cant_change_status_or_role_for_other_admin_error_msg()

    user.status = new_status
    await db.commit()
    await db.refresh(user)
    return user
 
 
# SWAP ROLE by ADMIN:
async def swap_user_role_by_admin_service(
        admin_id: int,
        user_to_swap_id: int,
        new_role: UserRoleEnum,
        db: AsyncSession,
)->User:
    """change user role as admin

    Args:
        admin_id (int): the current_user ADMIN ID
        user_to_swap_id (int): user you want to swap ID
        new_role (UserRoleEnum): role you want to setup
        db (AsyncSession): databse (async)

    Returns:
        User: updated user with new role.
    """
    
    if admin_id == user_to_swap_id:
        admin_cant_self_change_role_error_msg()
    
    user = await get_user_by_id_or_404(user_id=user_to_swap_id, db=db)

    if user.role == UserRoleEnum.ADMIN:
        admin_cant_change_status_or_role_for_other_admin_error_msg()

    user.role = new_role
    await db.commit()
    await db.refresh(user)
    return user
    

# ==================== DELETE ============================#

# Delete user  by ID as ADMIN
async def soft_delete_user_by_id_as_admin_service(
        current_user: User,
        user_id: int, # user id to delete
        db: AsyncSession,
)->User:
    """soft delete a user as admin: 
   
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

    user_to_soft_deleted.soft_delete()

    await db.commit()
    await db.refresh(user_to_soft_deleted)

    return user_to_soft_deleted

    

 

# ----------------------------------- # 
# --------- PRACTITIONER ONLY ------- #
# ----------------------------------- #

# ==================== GET ===============================#

# ==================== POST ==============================#

# ==================== PUT ===============================#

# ==================== PATCH =============================#

# ==================== DELETE ============================#








