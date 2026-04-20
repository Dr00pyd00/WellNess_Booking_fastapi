from decimal import Decimal # mieux pour les prix, plus precis

from pydantic import BaseModel, Field

from app.core.models_mixins.mixin_status import StatusEnum
from app.practitioners.models import PractitionerSpecialtyEnum
from app.users.schemas import UserDataFromDbSchema
from app.practitioners.models import PractitionerSpecialtyEnum



# ============================= #
# ==== FORMS ================== #
# ============================= # 

# CREATION =================================
class PractitionerCreationFormSchema(BaseModel):

    speciality: PractitionerSpecialtyEnum

    is_remote_possible: bool 

    address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Adress <string>: 5 to 200 char."
    )

    price: Decimal 

    bio: str = Field(
        min_length=10,
        max_length=1000,
        description="Biography/Curriculum: 10 to 1000 char.",
        default=None
    )


# UPDATE =================================
class PractitionerUpdateFormSchema(BaseModel):

    speciality: PractitionerSpecialtyEnum | None = None

    is_remote_possible: bool  | None = None

    address: str = Field(
        min_length=5,
        max_length=200,
        description="Adress <string>: 5 to 200 char.",
        default=None
    )

    price: Decimal | None = None

    bio: str = Field(
        min_length=10,
        max_length=1000,
        description="Biography/Curriculum: 10 to 1000 char.",
        default=None
    )
    
# ============================= #
# ==== READS ================== #
# ============================= #

# PRACTITIONER ACCESS FROM DB:
class PractitionerDataFromDbSchema(BaseModel):

    model_config={"from_attributes":True}

    id: int
    speciality: PractitionerSpecialtyEnum
    is_remote_possible: bool
    address: str 
    price: Decimal | None = None
    bio: str | None = None 
    user_id: int 
    user_profile: UserDataFromDbSchema

# PRACTITIONER DATA FOR PATIENTS:
class PractitionerDataForPatientsSchema(BaseModel):

    model_config={"from_attributes":True}

    speciality: PractitionerSpecialtyEnum
    is_remote_possible: bool
    address: str 
    price: Decimal | None = None 
    bio: str | None = None




# ============================= #
# ==== FILTERS ================ #
# ============================= #

class PractitionerFilterSpecialityStatusDeletedSchema(BaseModel):
    speciality: PractitionerSpecialtyEnum | None = None
    status: StatusEnum | None = None
    see_deleted: bool = False
