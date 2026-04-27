from typing import Never
from fastapi import HTTPException, status

from app.core.models_mixins.mixin_status import StatusEnum



# =========== GENERICS ITEMS ERRORS ================================= #

# not found
def item_not_found_error_msg(item_name:str = "item")->Never:
    """raise HTTPException if item not found 

    Args:
        item_name (str, optional): object name in case. Defaults to "item".

    Raises:
        HTTPException: 404 NOT FOUND
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{item_name} not found !"
    )

# soft_deleted
def item_soft_deleted_error_msg(item_name:str = "item")->Never:
    """raise HTTPexception if item is soft-deleted

    Args:
        item_name (str, optional): object name in case. Defaults to "item".

    Raises:
        HTTPException: 409 CONFICT

    """
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{item_name} is soft-delted !"
    )

# already exist (Field) : ie = "email already exist"
def item_already_exist_field_error_msg(item_name:str = "item", field_name:str = "field")->Never:
    """raise HTTPException if item already exist

    Args:
        item_name (str, optional): name of object . Defaults to "item".
        field_name (str, optional): name of the field who detect existance. Defaults to "field".

    Raises:
        HTTPException: 409 CONFLICT
    """
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{item_name} already exist by => field <{field_name}> ."
    )


# users : no token or invalid token 
def no_token_or_invalid_token_error_msg()->Never:
    """raise HTTPExcetpion if invalid token / inexistant token

    Raises:
        HTTPException: 401 UNAUTHORIZED
    """
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="invalid token"
    )


# user_type unauthorized (StatusEnum)
def user_status_unauthorized_error_msg(user_status:StatusEnum)->Never:
    """raise HTTPException if user unauthorized

    Args:
        user_status (StatusEnum): status of the user 

    Raises:
        HTTPException: 403 FORBIDDEN
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"status <{user_status}> Unauthorized !"
    )
