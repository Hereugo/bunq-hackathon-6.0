from typing import List, Literal, Optional

from app.core.handle_route_errors import handle_exceptions
from app.core.types import Amount, CounterpartyPointer
from app.router.payments import CreatePaymentRequest
from bunq.sdk.model.generated.endpoint import SchedulePaymentApiObject
from bunq.sdk.model.generated.object_ import (
    AmountObject,
    PointerObject,
    SchedulePaymentEntryObject,
)
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/schedule_payments", tags=["schedule_payments"])


RecurrenceUnit = Literal["ONCE", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]


class ScheduleDetails(BaseModel):
    """Model representing schedule details for a payment."""

    time_start: str = Field(
        default="%Y-%m-%dT%H:%M:%SZ",
        description="Start time for the schedule",
    )
    time_end: Optional[str] = Field(
        default="%Y-%m-%dT%H:%M:%SZ",
        description="End time for the schedule",
    )
    recurrence_unit: RecurrenceUnit = Field(
        default="ONCE",
        description="The schedule recurrence unit, options: ONCE, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY",
    )
    recurrence_size: int = Field(
        1, description="Recurrence size for the schedule (e.g., every 1 day)"
    )


class CreateSchedulePaymentRequest(BaseModel):
    """Model for creating a new scheduled payment."""

    payment: CreatePaymentRequest = Field(
        ...,
        description="The payment details.",
    )
    schedule: ScheduleDetails = Field(
        ...,
        description="Schedule details for the payment",
    )
    purpose: str = Field(
        default="weird purpose text",
        description="The schedule purpose",
    )


@router.post("/")
@handle_exceptions
async def create_schedule_payment(
    payment: CreateSchedulePaymentRequest, monetary_account_id: Optional[int] = None
):
    """
    Create a new Scheduled Payment using the bunq API.

    This endpoint processes scheduled payment requests by validating the data
    and creating a scheduled payment through the bunq Schedule Payment API.
    """
    schedule_payment_id = SchedulePaymentApiObject.create(
        payment=SchedulePaymentEntryObject(
            amount=AmountObject(
                payment.payment.amount.value,
                payment.payment.amount.currency,
            ),
            counterparty_alias=PointerObject(
                payment.payment.counterparty.type,
                payment.payment.counterparty.value,
                payment.payment.counterparty.name,
            ),
            description=payment.payment.description,
        ),
        schedule={
            "time_start": payment.schedule.time_start,
            "time_end": payment.schedule.time_end,
            "recurrence_unit": payment.schedule.recurrence_unit,
            "recurrence_size": payment.schedule.recurrence_size,
        },
        monetary_account_id=monetary_account_id,
    ).value

    return {
        "message": "Scheduled payment created successfully",
        "schedule_payment_id": schedule_payment_id,
        "payment": payment,
    }


@router.get("/{schedule_payment_id}")
@handle_exceptions
async def get_schedule_payment(
    schedule_payment_id: int, monetary_account_id: Optional[int] = None
):
    """
    Retrieve a scheduled payment using the bunq API.

    This endpoint fetches scheduled payment details by validating the schedule payment ID
    and monetary account ID.
    """
    schedule_payment = SchedulePaymentApiObject.get(
        schedule_payment_id=schedule_payment_id, monetary_account_id=monetary_account_id
    ).value

    return {
        "message": "Scheduled payment retrieved successfully",
        "schedule_payment_id": schedule_payment_id,
        "schedule_payment": schedule_payment,
    }


@router.get("/")
@handle_exceptions
async def list_schedule_payments(monetary_account_id: Optional[int] = None):
    """
    List all scheduled payments for a monetary account.

    This endpoint retrieves all scheduled payments for a given monetary account.
    """
    schedule_payments = SchedulePaymentApiObject.list(
        monetary_account_id=monetary_account_id
    ).value

    return {
        "message": "Scheduled payments retrieved successfully",
        "schedule_payments": schedule_payments,
    }


@router.put("/{schedule_payment_id}", deprecated=True)
@handle_exceptions
async def update_schedule_payment(
    payment: CreateSchedulePaymentRequest,
    schedule_payment_id: int,
    monetary_account_id: Optional[int] = None,
):
    """
    Update an existing scheduled payment using the bunq API.

    This endpoint updates scheduled payment details by validating the schedule payment ID
    and monetary account ID.
    """
    update_id = SchedulePaymentApiObject.update(
        payment=SchedulePaymentEntryObject(
            amount=AmountObject(
                payment.payment.amount.value,
                payment.payment.amount.currency,
            ),
            counterparty_alias=PointerObject(
                payment.payment.counterparty.type,
                payment.payment.counterparty.value,
                payment.payment.counterparty.name,
            ),
            description=payment.payment.description,
        ),
        schedule={
            "time_start": payment.schedule.time_start,
            "time_end": payment.schedule.time_end,
            "recurrence_unit": payment.schedule.recurrence_unit,
            "recurrence_size": payment.schedule.recurrence_size,
        },
        schedule_payment_id=schedule_payment_id,
        monetary_account_id=monetary_account_id,
    ).value

    return {"message": "Scheduled payment updated successfully", "update_id": update_id}


@router.delete("/{schedule_payment_id}")
@handle_exceptions
async def delete_schedule_payment(
    schedule_payment_id: int, monetary_account_id: Optional[int] = None
):
    """
    Delete a scheduled payment using the bunq API.

    This endpoint deletes a scheduled payment by validating the schedule payment ID
    and monetary account ID.
    """
    delete_id = SchedulePaymentApiObject.delete(
        schedule_payment_id=schedule_payment_id, monetary_account_id=monetary_account_id
    ).value

    return {"message": "Scheduled payment deleted successfully", "delete_id": delete_id}
