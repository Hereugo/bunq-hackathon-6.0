from typing import List, Literal, Optional

from bunq.sdk.http.api_client import uuid
from bunq.sdk.model.generated.endpoint import (
    CardApiObject,
    CardBatchApiObject,
    CardBatchReplaceApiObject,
    CardCreditApiObject,
    CardDebitApiObject,
    CardNameApiObject,
    CardReplaceApiObject,
)
from bunq.sdk.model.generated.object_ import (
    CardBatchEntryObject,
    CardBatchReplaceEntryObject,
)
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions
from ..core.types import Amount

router = APIRouter(prefix="/cards", tags=["cards"])


CardStatus = Literal["ACTIVE", "DEACTIVATED", "LOST", "STOLEN", "CANCELLED"]
OrderStatus = Literal[
    "ACCEPTED_FOR_PRODUCTION",
    "DELIVERED_TO_CUSTOMER",
    "CARD_UPDATE_REQUESTED",
    "CARD_UPDATE_SENT",
    "CARD_UPDATE_ACCEPTED",
    "CARD_REQUEST_PENDING",
]
ProductType = Literal[
    "MAESTRO_DEBIT",
    "MASTERCARD_DEBIT",
    "MASTERCARD_TRAVEL",
    "MASTERCARD_BUSINESS",
    "MASTERCARD_GREEN",
    "MASTERCARD_TRANSLINK",
    "MASTERCARD_CREDIT_PREPAID",
    "MASTERCARD_METAL",
]


class CountryPermissionRequest(BaseModel):
    country: str = Field(default="", description="")
    expiry_date: str = Field(default="", description="")
    id: str = Field(default="", description="")


class PinCodeAssignmentRequest(BaseModel):
    type: Literal["PRIMARY", "SECONDARY", "TERTIARY"] = Field(
        default="PRIMARY",
        description="PIN type. Can be PRIMARY, SECONDARY or TERTIARY",
    )
    routing_type: Optional[str] = Field(default="", description="Routing type.")
    pin_code: str = Field(
        default="0000",
        description="The 4 digit PIN to be assigned to this account.",
    )
    monetary_account_id: Optional[int] = Field(
        ...,
        description="The ID of the monetary account to assign to this pin for the card.",
    )
    status: Optional[str] = Field(
        default="",
        description="The status of the card pin assignment.",
    )


class PrimaryAccountNumberRequest(BaseModel):
    id: Optional[int] = Field(..., description="The ID for this Virtual PAN.")
    description: Optional[str] = Field(
        default="this is PAN description",
        description="The description for this PAN.",
    )
    status: Optional[str] = Field(
        default="",
        description="The status for this PAN, only for Online Cards.",
    )
    monetary_account_id: Optional[int] = Field(
        ...,
        description="The ID of the monetary account to assign to this PAN, only for Online Cards.",
    )
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid1()),
        description="The UUID for this Virtual PAN.",
    )
    four_digit: str = Field(
        default="2620",
        description="The last four digits of the PAN.",
    )
    type: str = Field(
        default="",
        description="The type of the PAN.",
    )


class CardRequest(BaseModel):
    pin_code: str = Field(
        default="0000",
        description="The plaintext pin code. Requests require encryption to be enabled",
    )
    activation_code: str = Field(
        default="ACTIVE",
        description="DEPRECATED: Activate a card by setting status to ACTIVE when the order_status is ACCEPTED_FOR_PRODUCTION.",
    )
    status: CardStatus = Field(
        default="DEACTIVATED",
        description="The status to set for the card. Can be ACTIVE, DEACTIVATED, LOST, STOLEN or CANCELLED, and can only be set to LOST/STOLEN/CANCELLED when order status is ACCEPTED_FOR_PRODUCTION/DELIVERED_TO_CUSTOMER/CARD_UPDATE_REQUESTED/CARD_UPDATE_SENT/CARD_UPDATE_ACCEPTED. Can only be set to DEACTIVATED after initial activation, i.e. order_status is DELIVERED_TO_CUSTOMER/CARD_UPDATE_REQUESTED/CARD_UPDATE_SENT/CARD_UPDATE_ACCEPTED. Mind that all the possible choices (apart from ACTIVE and DEACTIVATED) are permanent and cannot be changed after.",
    )
    order_status: OrderStatus = Field(
        default="CARD_REQUEST_PENDING",
        description="The order status to set for the card. Set to CARD_REQUEST_PENDING to get a virtual card produced.",
    )
    card_limit: Amount = Field(
        ...,
        description="The spending limit of a card",
    )
    card_limit_atm: Amount = Field(
        ...,
        description="The ATM spending limit of a card",
    )
    country_permission: CountryPermissionRequest = Field(
        ...,
        description="The countries for which to grant (temporary) permissions to use the card",
    )
    pin_code_assignment: PinCodeAssignmentRequest = Field(
        ..., description="Array of Types, PINs, account IDs assigned to the card"
    )
    primary_account_numbers: List[PrimaryAccountNumberRequest] = Field(
        ..., description="Array of PANs and their attributes"
    )
    monetary_account_id_fallback: Optional[int] = Field(
        default=0,
        description="ID of the MA to be used as fallback for this card if insufficient balance. Fallback account is removed if not supplied.",
    )
    preferred_name_on_card: str = Field(
        default="CARD_NAME",
        description="The user's preferred name as it will be on the card.",
    )
    second_line: str = Field(
        default="SECOND LINE BOTTOM TEXT",
        description="the second line of text on the card",
    )
    cancellation_reason: str = Field(
        default="FUCK THIS SHIT",
        description="The reason for card cancellation.",
    )


class CardBatchEntryRequest(BaseModel):
    id: int = Field(
        default=0,
        description="The ID of the card that needs to be updated.",
    )
    status: str = Field(
        default="DEACTIVATED",
        description="The status to set for the card. Can be ACTIVE, DEACTIVATED, LOST, STOLEN or CANCELLED, and can only be set to LOST/STOLEN/CANCELLED when order status is ACCEPTED_FOR_PRODUCTION/DELIVERED_TO_CUSTOMER/CARD_UPDATE_REQUESTED/CARD_UPDATE_SENT/CARD_UPDATE_ACCEPTED. Can only be set to DEACTIVATED after initial activation, i.e. order_status is DELIVERED_TO_CUSTOMER/CARD_UPDATE_REQUESTED/CARD_UPDATE_SENT/CARD_UPDATE_ACCEPTED. Mind that all the possible choices (apart from ACTIVE and DEACTIVATED) are permanent and cannot be changed after.",
    )
    card_limit: Amount = Field(
        ...,
        description="The spending limit of a card",
    )
    card_limit_atm: Amount = Field(
        ...,
        description="The ATM spending limit of a card",
    )
    country_permission: CountryPermissionRequest = Field(
        ...,
        description="The countries for which to grant (temporary) permissions to use the card",
    )
    monetary_account_id_fallback: Optional[int] = Field(
        default=0,
        description="ID of the MA to be used as fallback for this card if insufficient balance. Fallback account is removed if not supplied.",
    )


class CardBatchReplaceEntryRequest(BaseModel):
    id: int = Field(
        default=0,
        description="The ID of the card that needs to be replaced.",
    )
    name_on_card: str = Field(
        default="NEW CARD NAME",
        description="The user's preferred name as it will be on the card.",
    )
    pin_code_assignment: List[PinCodeAssignmentRequest] = Field(
        ..., description="Array of Types, PINs, account IDs assigned to the card"
    )
    second_line: str = Field(
        default="NEW SECOND LINE BOTTOM TEXT",
        description="the second line of text on the card",
    )


class CardBatchRequest(BaseModel):
    cards: List[CardBatchEntryRequest] = Field(
        ..., description="Cards that need to be updated"
    )


class CardBatchReplaceRequest(BaseModel):
    cards: List[CardBatchReplaceEntryRequest] = Field(
        ..., description="Cards that need to be replaced"
    )


class AliasRequest(BaseModel):
    type: Literal["EMAIL", "PHONE_NUMBER", "IBAN"] = Field(
        default="EMAIL",
        description="The alias type, can be: EMAIL|PHONE_NUMBER|IBAN.",
    )
    value: str = Field(
        default="test+666879f7-66bf-448c-9767-4f71d45cf0d9@bunq.com",
        description="The alias value.",
    )
    name: str = Field(default="JOHN DOE", description="The alias name.")
    service: Optional[str] = Field(
        default="",
        description="The pointer service. Only required for external counterparties.",
    )


class CardCreditRequest(BaseModel):
    second_line: str = Field(
        default="SECOND LINE BOTTOM TEXT",
        description="The second line of text on the card, used as name/description for it. It can contain at most 17 characters and it can be empty.",
    )
    name_on_card: str = Field(
        default="JOHN DOE",
        description="The user's name as it will be on the card. Check 'card-name' for the available card names for a user.",
    )
    type: Literal["MASTERCARD"] = Field(
        default="MASTERCARD",
        description="The type of card to order. Can be MASTERCARD.",
    )
    product_type: ProductType = Field(
        default="MASTERCARD_CREDIT_PREPAID",
        description="The product type of the card to order.",
    )
    first_line: str = Field(
        default="FIRST LINE",
        description="The first line of text on the card, used as name/description for it. It can contain at most 17 characters and it can be empty.",
    )
    preferred_name_on_card: str = Field(
        default="JOHN DOE",
        description="The user's preferred name that can be put on the card.",
    )
    alias: AliasRequest = Field(
        ...,
        description="The pointer to the monetary account that will be connected at first with the card. Its IBAN code is also the one that will be printed on the card itself. The pointer must be of type IBAN.",
    )
    pin_code_assignment: List[PinCodeAssignmentRequest] = Field(
        ...,
        description="Array of Types, PINs, account IDs assigned to the card",
    )
    monetary_account_id_fallback: Optional[int] = Field(
        ...,
        description="ID of the MA to be used as fallback for this card if insufficient balance. Fallback account is removed if not supplied.",
    )
    order_status: str = Field(
        default="VIRTUAL_DELIVERY",
        description="The order status of this card. Can be CARD_REQUEST_PENDING or VIRTUAL_DELIVERY.",
    )


class CardDebitRequest(BaseModel):
    second_line: str = Field(
        default="SECOND LINE BOTTOM TEXT",
        description="The second line of text on the card, used as name/description for it. It can contain at most 17 characters and it can be empty.",
    )
    name_on_card: str = Field(
        default="JOHN DOE",
        description="The user's name as it will be on the card. Check 'card-name' for the available card names for a user.",
    )
    type: Literal["MAESTRO", "MASTERCARD"] = Field(
        default="MASTERCARD",
        description="The type of card to order. Can be MASTERCARD.",
    )
    product_type: ProductType = Field(
        default="MASTERCARD_DEBIT",
        description="The product type of the card to order.",
    )
    preferred_name_on_card: str = Field(
        default="JOHN DOE",
        description="The user's preferred name that can be put on the card.",
    )
    alias: AliasRequest = Field(
        ...,
        description="The pointer to the monetary account that will be connected at first with the card. Its IBAN code is also the one that will be printed on the card itself. The pointer must be of type IBAN.",
    )
    pin_code_assignment: List[PinCodeAssignmentRequest] = Field(
        ...,
        description="Array of Types, PINs, account IDs assigned to the card",
    )
    monetary_account_id_fallback: Optional[int] = Field(
        ...,
        description="ID of the MA to be used as fallback for this card if insufficient balance. Fallback account is removed if not supplied.",
    )
    order_status: str = Field(
        default="VIRTUAL_DELIVERY",
        description="The order status of this card. Can be CARD_REQUEST_PENDING or VIRTUAL_DELIVERY.",
    )


class CardReplaceRequest(BaseModel):
    second_line: str = Field(
        default="SECOND LINE BOTTOM TEXT",
        description="The second line of text on the card, used as name/description for it. It can contain at most 17 characters and it can be empty.",
    )
    name_on_card: str = Field(
        default="JOHN DOE",
        description="The user's name as it will be on the card. Check 'card-name' for the available card names for a user.",
    )
    preferred_name_on_card: str = Field(
        default="JOHN DOE",
        description="The user's preferred name that can be put on the card.",
    )
    pin_code_assignment: List[PinCodeAssignmentRequest] = Field(
        ...,
        description="Array of Types, PINs, account IDs assigned to the card",
    )


@router.post("/card_credit")
@handle_exceptions
async def create_card_credit(card_credit: CardCreditRequest):
    """
    Create a new credit card request.
    """
    card_credit_res = CardCreditApiObject.create(
        second_line=card_credit.second_line,
        name_on_card=card_credit.name_on_card,
        type_=card_credit.type,
        product_type=card_credit.product_type,
        first_line=card_credit.first_line,
        preferred_name_on_card=card_credit.preferred_name_on_card,
        alias=card_credit.alias,
        pin_code_assignment=card_credit.pin_code_assignment,
        monetary_account_id_fallback=card_credit.monetary_account_id_fallback,
        order_status=card_credit.order_status,
    ).value

    return card_credit_res


@router.post("/card_debit")
@handle_exceptions
async def create_card_debit(card_debit: CardDebitRequest):
    """
    Create a new credit card request.
    """
    card_debit_res = CardDebitApiObject.create(
        second_line=card_debit.second_line,
        name_on_card=card_debit.name_on_card,
        type_=card_debit.type,
        product_type=card_debit.product_type,
        preferred_name_on_card=card_debit.preferred_name_on_card,
        alias=card_debit.alias,
        pin_code_assignment=card_debit.pin_code_assignment,
        monetary_account_id_fallback=card_debit.monetary_account_id_fallback,
        order_status=card_debit.order_status,
    ).value

    return card_debit_res


@router.post("/batch")
@handle_exceptions
async def update_card_batch(card_batch: CardBatchRequest):
    """
    Used to update multiple cards in a batch.
    """
    card_batch_res = CardBatchApiObject.create(
        cards=[
            CardBatchEntryObject(
                id_=card.id,
                status=card.status,
                card_limit=card.card_limit,
                card_limit_atm=card.card_limit_atm,
                country_permission=card.country_permission,
                monetary_account_id_fallback=card.monetary_account_id_fallback,
            )
            for card in card_batch.cards
        ]
    ).value
    return card_batch_res


@router.post("/batch_replace")
@handle_exceptions
async def card_batch_replace(card_batch_replace: CardBatchReplaceRequest):
    """
    Used to replace multiple cards in a batch.
    """
    card_batch_replace_res = CardBatchReplaceApiObject.create(
        cards=[
            CardBatchReplaceEntryObject(
                id_=card.id,
                name_on_card=card.name_on_card,
                pin_code_assignment=card.pin_code_assignment,
                second_line=card.second_line,
            )
            for card in card_batch_replace.cards
        ]
    ).value

    return card_batch_replace_res


@router.put("/")
@handle_exceptions
async def update_card(
    card: CardRequest,
    card_id: int,
):
    """
    Update the card details. Allow to change pin code, status, limits, country permissions and the monetary account connected to the card.
    When the card has been received, it can be also activated through this endpoint.
    """
    # Update draft payment using BunQ SDK
    card = CardApiObject.update(
        card_id=card_id,
        pin_code=card.pin_code,
        activation_code=card.activation_code,
        status=card.status,
        order_status=card.order_status,
        card_limit=card.card_limit,
        card_limit_atm=card.card_limit_atm,
        country_permission=card.country_permission,
        pin_code_assignment=card.pin_code_assignment,
        primary_account_numbers=card.primary_account_numbers,
        monetary_account_id_fallback=card.monetary_account_id_fallback,
        preferred_name_on_card=card.preferred_name_on_card,
        second_line=card.second_line,
        cancellation_reason=card.cancellation_reason,
    ).value

    return card


@router.post("/card_replace")
@handle_exceptions
async def replace_card(card_replace: CardReplaceRequest, card_id: int):
    """
    Request a card replacement.
    """
    card = CardReplaceApiObject.create(
        card_id=card_id,
        name_on_card=card_replace.name_on_card,
        preferred_name_on_card=card_replace.preferred_name_on_card,
        pin_code_assignment=card_replace.pin_code_assignment,
        second_line=card_replace.second_line,
    ).value
    return card


@router.get("/{card_id}")
@handle_exceptions
async def get_card(card_id: int):
    """
    Retrieve a card using the bunq API.

    This endpoint fetches card details by validating the card and monetary account ID.
    """
    card = CardApiObject.get(
        card_id=card_id,
    ).value

    return card


@router.get("/")
@handle_exceptions
async def list_cards():
    """
    List all cards.

    This endpoint retrieves all cards.
    """
    cards = CardApiObject.list(
        # params=params
    ).value

    return cards


@router.get("/card_names")
@handle_exceptions
async def list_card_names():
    """
    Return all the accepted card names for a specific user.
    """
    card_names = CardNameApiObject.list(
        # params=params
    ).value

    return card_names
