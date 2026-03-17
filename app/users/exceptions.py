from fastapi import HTTPException, status


def try_soft_delete_last_admin_error_msg():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You can't delete last admin"
    )


def  non_admin_user_try_delete_other_user_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user can't delete other user."
    )


def user_already_soft_deleted_error_msg(user_id:int):
    raise HTTPException(
        status.HTTP_409_CONFLICT,
        detail=f"user ID:{user_id} already soft-deleted."
    )

def user_try_patch_other_user_error_msg(current_user_id:int, user_to_patch_id:int):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"user ID:{current_user_id} can't modify user ID:{user_to_patch_id} profile."
    )

def user_try_update_pw_but_old_wrong_error_msg(user_id:int):
    raise HTTPException(
        status.HTTP_409_CONFLICT,
        detail=f"user ID:{user_id} wrong old password."
    )