from typing import Optional

from bunq.sdk.model.generated.endpoint import PaymentApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions
from ..core.types import Amount, CounterpartyPointer

router = APIRouter(prefix="/payments", tags=["payments"])


class CreatePaymentRequest(BaseModel):
    """Model for creating a new payment."""

    amount: Amount = Field(
        ..., description="Amount information including value and currency"
    )
    counterparty: CounterpartyPointer = Field(
        ..., description="Counterparty (recipient) information"
    )
    description: str = Field(..., description="Payment description", max_length=140)


@router.post("/")
@handle_exceptions
async def create_payment(
    payment: CreatePaymentRequest,
    monetary_account_id: Optional[int] = None,
):
    """
    Create a new Payment using the bunq API.

    This endpoint processes payment requests by validating the data
    and creating a payment through the bunq Payment API.
    """
    payment_id = PaymentApiObject.create(
        amount=AmountObject(payment.amount.value, payment.amount.currency),
        counterparty_alias=PointerObject(
            payment.counterparty.type,
            payment.counterparty.value,
            payment.counterparty.name,
        ),
        description=payment.description,
        monetary_account_id=monetary_account_id,
    ).value

    return {
        "message": "Payment created successfully",
        "payment_id": payment_id,
        "payment": payment,
    }


@router.get("/{payment_id}")
@handle_exceptions
async def get_payment(payment_id: int, monetary_account_id: Optional[int] = None):
    """
    Retrieve a payment using the bunq API.

    This endpoint fetches payment details by validating the payment ID
    and monetary account ID.
    """
    payment = PaymentApiObject.get(
        payment_id=payment_id,
        monetary_account_id=monetary_account_id,
    ).value

    return {
        "message": "Payment recieved successfully",
        "payment_id": payment_id,
        "payment": payment,
    }


@router.get("/")
@handle_exceptions
async def list_payments(monetary_account_id: Optional[int] = None):
    """
    List all payments for a monetary account.

    This endpoint retrieves all payments (both incoming and outgoing)
    performed on a given monetary account.
    """
    payments = PaymentApiObject.list(monetary_account_id=monetary_account_id).value

    return {"message": "Payments retrieved successfully", "payments": payments}
