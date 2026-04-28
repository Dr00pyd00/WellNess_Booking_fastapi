from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class SoftDeleteMixin():
    """Soft delete mixin:

        Row deleted_at:

            - None if not deleted

            - datetime if deleted
            """

    deleted_at: Mapped[datetime | None] = mapped_column(
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

