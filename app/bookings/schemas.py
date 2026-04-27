
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from app.availabilities.schemas import AvailabilityUserReservationViewSchema
from app.core.models_mixins.mixin_status import StatusEnum
from app.users.schemas import UserDataFromDbSchema



# ============================= #
# ==== FORMS ================== #
# ============================= # 

# TAKE A RDV (BOOKING) =================================
class TakeBookingByPatientFormSchema(BaseModel):

    availability_id: int

    message_to_practitioner: str = Field(
        min_length=5,
        max_length=800,
        description="Message <string>: 5 to 800 chars.",
        default=None,
    )


# ============================= #
# ==== READS ================== #
# ============================= #

# ========= PRACTITIONER SEE PATIENT BOOKING ===============
class PatientBookingDataForPractitionerSchema(BaseModel):

    model_config={"from_attributes":True}

    id: int
    user_profile: UserDataFromDbSchema
    availability: AvailabilityUserReservationViewSchema
    message_to_practitioner: str | None = None
    created_at: datetime
    deleted_at: datetime | None


# FILTERS 
class BookingFilterStatusDeletedBookedPractPatientSchema(BaseModel):
    status: List[StatusEnum] | None = None
    see_deleted: bool = False
    by_practitioner: int | None = None
    by_patient: int | None = None

