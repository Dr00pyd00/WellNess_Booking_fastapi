import enum as PyEnum

from sqlalchemy import Column, Enum

# enum pour les status :
class StatusEnum(PyEnum):

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    SIGNALED = "SIGNALED"
    REPORTED = "REPORTED"


class StatusMixin():

    status = Column(
        Enum,
        nullable=False,
        server_default=StatusEnum.ACTIVE,
        default=StatusEnum.ACTIVE,

    )




