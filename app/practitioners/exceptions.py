
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