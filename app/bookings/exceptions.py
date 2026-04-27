from typing import Never
from fastapi import status, HTTPException




def user_try_take_already_booked_slot_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This availability already booked."
    )

def user_try_take_slot_in_past_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This availability is passed."
    )

def user_try_delete_booking_not_owner_error_msg()->Never:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user is not the booking owner, can't delete it."
    )
