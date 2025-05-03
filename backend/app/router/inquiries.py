from typing import Optional

from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions
from ..core.types import Amount, CounterpartyPointer

router = APIRouter(prefix="/request_inquiries", tags=["request_inquiries"])


class CreateRequestInquiryRequest(BaseModel):
    """Model for creating a new request inquiry."""

    amount: Amount = Field(
        ..., description="Amount information including value and currency"
    )
    counterparty: CounterpartyPointer = Field(
        ..., description="Counterparty (recipient) information"
    )
    description: str = Field(...,
                             description="Request description", max_length=140)


@router.post("/")
@handle_exceptions
async def create_request_inquiry(inquiry: CreateRequestInquiryRequest):
    """
    Create a new Request Inquiry using the bunq API.

    This endpoint processes request inquiries by validating the data
    and creating a request through the bunq Request Inquiry API.
    """
    inquiry_id = RequestInquiryApiObject.create(
        amount_inquired=AmountObject(
            inquiry.amount.value, inquiry.amount.currency),
        counterparty_alias=PointerObject(
            inquiry.counterparty.type,
            inquiry.counterparty.value,
            inquiry.counterparty.name,
        ),
        description=inquiry.description,
        allow_bunqme=False,
    ).value

    return {"message": "Request inquiry created successfully", "inquiry_id": inquiry_id}


@router.get("/{inquiry_id}")
@handle_exceptions
async def get_request_inquiry(
    inquiry_id: int, monetary_account_id: Optional[int] = None
):
    """
    Retrieve a request inquiry using the bunq API.

    This endpoint fetches request inquiry details by validating the inquiry ID
    and monetary account ID.
    """
    inquiry = RequestInquiryApiObject.get(
        request_inquiry_id=inquiry_id, monetary_account_id=monetary_account_id
    ).value

    return {"inquiry": inquiry, "inquiry_id": inquiry_id}


@router.get("/")
@handle_exceptions
async def list_request_inquiries(monetary_account_id: Optional[int] = None):
    """
    List all request inquiries for a monetary account.

    This endpoint retrieves all request inquiries performed
    on a given monetary account.
    """
    inquiries = RequestInquiryApiObject.list(
        monetary_account_id=monetary_account_id
    ).value

    return {"inquiries": inquiries}
