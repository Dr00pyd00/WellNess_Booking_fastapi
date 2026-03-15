import enum as PyEnum

from sqlalchemy import Column, Enum

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

    status = Column(
        Enum,
        nullable=False,
        server_default=StatusEnum.ACTIVE,
        default=StatusEnum.ACTIVE,

    )




