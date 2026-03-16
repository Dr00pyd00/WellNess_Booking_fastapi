from datetime import time

from pydantic import BaseModel, Field

from app.availabilities.models import DaysEnum
from app.practitioners.schemas import PractitionerDataForPatientsSchema


# ============================= #
# ==== FORMS ================== #
# ============================= # 

# CREATION =================================
class AvailabilityCreationFormSchema(BaseModel):

    day: DaysEnum = Field(
        ...,
        description="Chose day for rendez vous."
    )

    start_time: time = Field(
        ...,
        description="Time when rendez vous start."
    )

    end_time: time = Field(
        ...,
        description="Time when rendez vous end."
    )


# ============================= #
# ==== READS ================== #
# ============================= #

# USER CAN SEE WHEN HE WANT TO LOCK RDV:
class AvailabilityUserReservationViewSchema(BaseModel):

    model_config={"from_attributes":True}

    day: DaysEnum
    start_time: time 
    end_time: time 
    practitioner_id: int

