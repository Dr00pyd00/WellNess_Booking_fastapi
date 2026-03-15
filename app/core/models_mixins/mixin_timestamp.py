from sqlalchemy import Column, DateTime, func



class TimeStampMixin():
    """Mixin to add 2 rows:

        -created_at (datetime)

        -updated_at (datetime)
    """

    create_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),

    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),

    )
