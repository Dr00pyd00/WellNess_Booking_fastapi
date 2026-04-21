
from fastapi import HTTPException, status


def try_create_practitioner_profile_when_not_practitioner_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Can't create practitioner because you not a practitioner."
    )

def try_create_practitioner_profile_when_already_have_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This user already have profile page."
    )


def try_update_inexistant_profile_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This account don't have practitioner profile."
    )

def user_try_update_pract_not_own_error_msg():
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user is not the practitioner profile owner."
            )

def user_try_delete_pract_not_own_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This user is not the practitioner profile owner."
    )

def user_try_delete_own_pract_profile_already_soft_deleted_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="the practitioner profile already soft deleted. "
    )