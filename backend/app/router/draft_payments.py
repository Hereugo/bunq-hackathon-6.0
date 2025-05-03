from datetime import datetime
from typing import List, Literal, Optional

from bunq.sdk.model.generated.endpoint import DraftPaymentApiObject
from bunq.sdk.model.generated.object_ import (
    AmountObject,
    DraftPaymentEntryObject,
    PointerObject,
)
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions
from ..core.types import Amount, CounterpartyPointer

router = APIRouter(prefix="/draft_payments", tags=["draft_payments"])


class EntriesRequest(BaseModel):
    amount: Amount = Field(
        default=Amount(value="10.00", currency="EUR"),
        description="Amount information including value and currency",
    )
    counterparty_alias: CounterpartyPointer = Field(
        ...,
        description="The LabelMonetaryAccount containing the public information of the other (counterparty) side of the DraftPayment",
    )
    description: str = Field(
        default="this is a description",
        description="description for DraftPayment",
        max_length=140,
    )
    # merchant_reference: str = Field(
    #    ...,
    #    description="Optional data to be included with the Payment specific to the merchant.",
    # )
    # attachment: List[Attachment]
    # id
    # alias
    # type


class DraftPaymentRequest(BaseModel):
    """Model for creating a new draft payment."""

    status: Optional[Literal["ACCEPTED", "PENDING", "REJECTED"]] = Field(
        default="PENDING",
        description="The status of the DraftPayment.",
    )
    entries: List[EntriesRequest] = Field(
        ...,
        description="The list of entries in the DraftPaymen.t each entry will result in a payment when the DraftPayment is accepted.",
    )
    previous_updated_timestamp: Optional[str] = Field(
        default="2025-05-02T23:58:09.021923",
        description="the last updated_timestamp that you received of this DraftPayment. This needs to be provided to prevent race conditions.",
    )
    number_of_required_accepts: int = Field(
        default=1,
        description="The number of accepts that are required for the draft payment to receive status ACCEPTED. Currently only 1 is valid.",
    )
    # schedule


@router.post("/")
@handle_exceptions
async def create_draft_payment(
    draft_payment: DraftPaymentRequest,
    monetary_account_id: Optional[int] = None,
):
    """
    Create a new draft Payment using the BunQ API.

    This endpoint processes draft payment requests by validating the data
    and creating a draft payment through the BunQ Draft Payment API.
    """
    # Create draft payment using BunQ SDK
    draft_payment = DraftPaymentApiObject.create(
        monetary_account_id=monetary_account_id,
        status=draft_payment.status,
        entries=[
            DraftPaymentEntryObject(
                amount=AmountObject(entry.amount.value, entry.amount.currency),
                counterparty_alias=PointerObject(
                    entry.counterparty_alias.type,
                    entry.counterparty_alias.value,
                    entry.counterparty_alias.name,
                ),
                description=entry.description,
                # merchant_reference=entry.merchant_reference
                # attachment=entry.attachment
            )
            for entry in draft_payment.entries
        ],
        previous_updated_timestamp=draft_payment.previous_updated_timestamp,
        number_of_required_accepts=draft_payment.number_of_required_accepts,
        # schedule
    ).value

    return draft_payment


@router.put("/")
@handle_exceptions
async def update_draft_payment(
    draft_payment_id: int,
    status: Literal["ACCEPTED", "PENDING", "REJECTED"],
    monetary_account_id: Optional[int] = None,
):
    """
    Updates the status of the specified draft payment to "ACCEPTED", indicating your approval.
    If the draft payment requires multiple approvals (as specified by number_of_required_accepts),
    it will only be executed once the required number of users have accepted it.
    """
    # Update draft payment using BunQ SDK
    draft_payment = DraftPaymentApiObject.update(
        status=status,
        draft_payment_id=draft_payment_id,
        monetary_account_id=monetary_account_id,
    ).value

    return draft_payment


@router.get("/{draft_payment_id}")
@handle_exceptions
async def get_draft_payment(
    draft_payment_id: int, monetary_account_id: Optional[int] = None
):
    """
    Retrieve a draft payment using the bunq API.

    This endpoint fetches draft payment details by validating the draft payment ID
    and monetary account ID.
    """
    draft_payment = DraftPaymentApiObject.get(
        draft_payment_id=draft_payment_id,
        monetary_account_id=monetary_account_id,
    ).value

    return draft_payment


@router.get("/")
@handle_exceptions
async def list_payments(monetary_account_id: Optional[int] = None):
    """
    List all payments for a monetary account.

    This endpoint retrieves all payments (both incoming and outgoing)
    performed on a given monetary account.
    """
    draft_payments = DraftPaymentApiObject.list(
        monetary_account_id=monetary_account_id
    ).value

    return draft_payments
