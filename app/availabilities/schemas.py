from datetime import time
from datetime import date as d_date

from pydantic import BaseModel, Field

from app.availabilities.models import DaysEnum
from app.practitioners.schemas import PractitionerDataForPatientsSchema


# ============================= #
# ==== FORMS ================== #
# ============================= # 

# CREATION =================================
class AvailabilityCreationFormSchema(BaseModel):

    # day: DaysEnum = Field(
    #     ...,
    #     description="Chose day for rendez vous."
    # )

    date: d_date = Field(
        ...,
        description="date of the slot."
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

