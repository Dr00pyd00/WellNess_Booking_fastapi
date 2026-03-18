from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.jwt import verify_jwt_token
from app.dependencies.database import get_db
from app.users.exceptions import current_user_is_soft_deleted_error_msg, user_dont_have_required_role_error_msg
from app.users.models import User, UserRoleEnum
from app.users.services import get_user_by_id_or_404


# Cherche automatiquement un Bearer token dans le header:
    # si pas de token : raise 401 unauthorize auto!
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
        )->User: 
    """take token bearer in header , check and return user or errors.

    Args:
        token (Annotated[str, Depends): Bearer Token
        db (Annotated[AsyncSession, Depends): database Session

    Returns:
        User: current_user   
        or   
        Raise HTTPExceptions
    """
    
    current_user_id = verify_jwt_token(token=token).user_id
    current_user = await  get_user_by_id_or_404(user_id=current_user_id, db=db)
    
    # check si soft deleted:
    if current_user.deleted_at is not None:
        current_user_is_soft_deleted_error_msg(id=current_user_id)
    
    return current_user



# Depends avec Closure et List de roles possible pour filtrer des autorisations:
    # Depends ne prend jamais d'arg => required_roles est lancer en premier avec que depends ne proc.
def required_roles(*required_role:UserRoleEnum):
    def check_current_user_role(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in required_role:
            user_dont_have_required_role_error_msg()
        return current_user
    return check_current_user_role
