
from pydantic import BaseModel, Field

from app.availabilities.schemas import AvailabilityUserReservationViewSchema
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
