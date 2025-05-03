from typing import Optional

from bunq.sdk.model.generated.endpoint import BillingContractSubscriptionApiObject
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions

router = APIRouter(
    prefix="/billing_contract_subscription", tags=["billing_contract_subscription"]
)


class BillingContractSubscription(BaseModel):
    """Model representing a billing contract subscription."""

    subscription_type: Optional[str] = Field(
        None,
        description="The subscription type of the user. Can be one of "
        "PERSON_SUPER_LIGHT_V1, PERSON_LIGHT_V1, PERSON_MORE_V1, "
        "PERSON_FREE_V1, PERSON_PREMIUM_V1, COMPANY_V1, or COMPANY_V2.",
    )
    id: Optional[int] = Field(None, description="The id of the billing contract.")
    created: Optional[str] = Field(
        None, description="The timestamp when the billing contract was made."
    )
    updated: Optional[str] = Field(
        None, description="The timestamp when the billing contract was last updated."
    )
    contract_date_start: Optional[str] = Field(
        None, description="The date from when the billing contract is valid."
    )
    contract_date_end: Optional[str] = Field(
        None, description="The date until when the billing contract is valid."
    )
    contract_version: Optional[int] = Field(
        None, description="The version of the billing contract."
    )
    subscription_type_downgrade: Optional[str] = Field(
        None, description="The subscription type the user will have after a downgrade."
    )
    status: Optional[str] = Field(None, description="The subscription status.")
    sub_status: Optional[str] = Field(None, description="The subscription substatus.")


@router.get("/")
@handle_exceptions
async def get_billing_contract_subscription(user_id: Optional[int] = None):
    """
    Retrieve the subscription billing contract for the authenticated user.

    This endpoint fetches the billing contract subscription details
    for the specified user or the authenticated user if not specified.
    """
    billing_contract_subscriptions = BillingContractSubscriptionApiObject.list(
        user_id=user_id
    ).value

    return {"billing_contract_subscriptions": billing_contract_subscriptions}
