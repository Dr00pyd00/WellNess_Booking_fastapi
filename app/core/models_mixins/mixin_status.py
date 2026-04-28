from enum import Enum as PyEnum

from sqlalchemy import Enum 
from sqlalchemy.orm import Mapped, mapped_column

# enum pour les status :
class StatusEnum(PyEnum):

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    SIGNALED = "SIGNALED"
    REPORTED = "REPORTED"


class StatusMixin():
    """Mixin for status:

    -ACTIVE = normal flow

    -ARCHIVED = in db but not accessible (just by admins)

    -SIGNALED = report done but not analysed

    -REPORTED = out of app
    
    """

    status : Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name="status_enum"),
        server_default="ACTIVE",
        default=StatusEnum.ACTIVE,
            )

    @classmethod
    def active_only(cls):
        return cls.status == StatusEnum.ACTIVE



