from sqlalchemy import Column, DateTime, func


class SoftDeleteMixin():
    """Soft delete mixin:

        Row deleted_at:

            - None if not deleted

            - datetime if deleted
            """

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,

    )

    def soft_delete(self):
        self.deleted_at = func.now()

    def restore_from_soft_delete(self):
        self.deleted_at = None

    @classmethod
    def not_deleted_only(cls):
        return cls.deleted_at.is_(None)