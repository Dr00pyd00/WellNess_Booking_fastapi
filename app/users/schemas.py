import re
from typing import Optional
from datetime import date, datetime
from dateutil.relativedelta import relativedelta  # prend en compteannées bisectiles

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.models_mixins.mixin_status import StatusEnum
from app.users.models import UserRoleEnum



# ============================= #
# ==== READS ================== #
# ============================= #

# USER ACCESS FROM DB:
class UserDataFromDbSchema(BaseModel):

    model_config={"from_attributes":True}

    id: int
    username: str
    name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    birth: date | None = None 
    role: UserRoleEnum 
    status: StatusEnum
    created_at: datetime
    deleted_at: datetime | None 

# ALL DATA NO SECURITY FROM DB:
class UserFullDataFromDbSchema(UserDataFromDbSchema):
    password: str





# ============================= #
# ==== FORMS ================== #
# ============================= # 

# CREATION =================================
class UserCreationFormSchema(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username <string>: 3 to 50 chars."
    )

    name: Optional[str] = Field(
        min_length=2,
        max_length=80,
        description="Name <string>: 2 to 80 chars.",
        default=None,

    ) 

    password: str = Field(
        ...,
        min_length=5,
        max_length=150,
        description="Password <string>: 5 to 150 chars."
    )

    email: EmailStr = Field(
        ...,
        description="user email for communicate patient/practitioner/admin."
    )

    birth: Optional[date] = None

    phone_number: Optional[str] = None


    # validateurs :

    @field_validator("username")
    @classmethod
    def verify_username_is_alphanumeric(cls, input:str)->str:
        if re.match(r'^[a-zA-Z0-9_-]+$', input) is None:
            raise ValueError("<username> must be alphanumeric (can contain - and _)")
        return input

    @field_validator("password")
    @classmethod
    def verify_passowrd_complexity(cls, input:str)->str:
        if not any(char.isdigit() for char in input):
            raise ValueError("<password> must containt at least ONE digit.")
        if not any(char.isalpha() for char in input):
            raise ValueError("<password> must contain at least ONE alpha char.")
        return input
    
    @field_validator("birth")
    @classmethod
    def verify_age_possible(cls, input):
        if input >= date.today():
            raise ValueError("<birth> must be greater than Now.")
        if input <= date.today() - relativedelta(years=120) :
            raise ValueError("<birth>, your age can't be greater than 120 years")
        return input


# LOGIN =================================
class UserLoginFormSchema(BaseModel):
    username: str
    password: str

# UPDATE STATUS FORM =====================
class UserSwapStatusFormSchema(BaseModel):
    new_status: StatusEnum

# UPDATE ROLE FORM =======================
class UserSwapRoleFormSchema(BaseModel):
    new_role: UserRoleEnum


# UPDATE PASSWORD WITH VERIFICATION OLD ONE 
class UserUpdatePasswordFormSchema(BaseModel):
    old_password: str = Field(
        ...,
        min_length=5,
        max_length=150,
        description="The current password <string>: 5 to 150 chars."
    )

    new_password: str = Field(
        ...,
        min_length=5,
        max_length=150,
        description="New Password <strin>: 5 to 150 chars.",
    )

    @field_validator("new_password")
    @classmethod
    def verify_passowrd_complexity(cls, input:str)->str:
        if not any(char.isdigit() for char in input):
            raise ValueError("<passwor> must containt at least ONE digit.")
        if not any(char.isalpha() for char in input):
            raise ValueError("<password> must contain at least ONE alpha char.")
        return input
    

# UPDATE PROFILE =========================
class UserUpdateProfileFormSchema(BaseModel):

    username: Optional[str] = Field(
        min_length=3,
        max_length=50,
        description="Username <string>: 3 to 50 chars.",
        default=None
    ) 

    name: Optional[str] = Field(
        min_length=2,
        max_length=80,
        description="Name <string>: 2 to 80 chars.",
        default=None,

    ) 

    email: Optional[EmailStr] = None

    birth: Optional[date] = None

    phone_number: Optional[str] = None

    # validations:

    @field_validator("username")
    @classmethod
    def verify_username_is_alphanumeric(cls, input:str)->str:
        if re.match(r'^[a-zA-Z0-9_-]+$', input) is None:
            raise ValueError("<username> must be alphanumeric (can contain - and _)")
        return input


    @field_validator("birth")
    @classmethod
    def verify_age_possible(cls, input):
        if input >= date.today():
            raise ValueError("<birth> must be greater than Now.")
        if input <= date.today() - relativedelta(years=120) :
            raise ValueError("<birth>, your age can't be greater than 120 years")
        return input



# ================================================= #
# ============= FILTERS =========================== # 
# ================================================= #

class UserFilterRoleStatusDeletedSchema(BaseModel):
    role: UserRoleEnum | None = None
    status: StatusEnum | None = None 
    see_deleted: bool = False


