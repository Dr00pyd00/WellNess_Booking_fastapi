from fastapi import status, HTTPException




def user_try_take_already_booked_slot_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This availability already booked."
    )

def user_try_take_slot_in_past_error_msg():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This availability is passed."
    )