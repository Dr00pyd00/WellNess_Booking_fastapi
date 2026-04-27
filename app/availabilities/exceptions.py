from typing import Never
from fastapi import HTTPException, status


def user_try_to_create_avail_when_not_the_practitioner_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user is not the practitioner."
    )


def pract_try_soft_delete_inexistant_avail_slot_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The practitioner try delete inexistant avail slot."
    )


def pract_try_soft_delete_not_own_avail_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The current practitioner is not the avail owner."
    )

def avail_already_soft_deleted_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This availability already soft deleted."
    )

def try_find_avail_but_inactive_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Availability inactive."
    )



def try_find_avail_but_deleted_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Availability soft_deleted."
    )


def try_find_avail_but_inexistant_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Availability inexistant."
    )

