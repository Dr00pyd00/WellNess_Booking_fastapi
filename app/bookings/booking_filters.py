from typing import Annotated

from fastapi import Query

from app.bookings.schemas import BookingFilterStatusDeletedBookedPractPatientSchema
from app.core.models_mixins.mixin_status import StatusEnum


def get_booking_filters_status_deleted_bypatient_by_practitioner(
        status: Annotated[StatusEnum | None, Query(description="query for filter <status>.")] = None,
        see_deleted: Annotated[bool, Query(description="query for <see_deleted>.If True: show deleted bookings.")] = False,
        by_practitioner: Annotated[int, Query(description="practitioner ID booking owner you want to see only. ")] = None,
        by_patient: Annotated[int, Query(description="patient ID booking owner you want to see only. ")] = None,
)->BookingFilterStatusDeletedBookedPractPatientSchema:
    
    return BookingFilterStatusDeletedBookedPractPatientSchema(
        status=status,
        see_deleted=see_deleted,
        by_practitioner=by_practitioner,
        by_patient=by_patient
    )
