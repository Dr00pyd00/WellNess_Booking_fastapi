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