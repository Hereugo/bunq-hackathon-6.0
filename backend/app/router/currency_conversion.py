from typing import List, Literal, Optional

from bunq.sdk.model.generated.endpoint import (
    CurrencyConversionApiObject,
    CurrencyConversionQuoteApiObject,
)
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions
from ..core.types import Amount, CounterpartyPointer

router = APIRouter(prefix="/currency_conversion", tags=["currency_conversion"])


class CurrencyConversionQuoteRequest(BaseModel):
    """Model for creating a currency conversion quote."""

    amount: Amount = Field(..., description="The amount to convert")
    currency_source: str = Field(..., description="The currency we are converting from")
    currency_target: str = Field(..., description="The currency we are converting to")
    order_type: Literal["SELL", "BUY"] = Field(
        ..., description="The type of the quote, SELL or BUY"
    )
    counterparty: CounterpartyPointer = Field(
        ..., description="Counterparty information"
    )


class CurrencyConversionQuoteStatusUpdate(BaseModel):
    """Model for updating a currency conversion quote's status."""

    status: Literal["ACCEPTED", "REJECTED"] = Field(
        ..., description="The status of the quote"
    )


@router.post("/quotes")
@handle_exceptions
async def create_currency_conversion_quote(
    quote: CurrencyConversionQuoteRequest, monetary_account_id: Optional[int] = None
):
    """
    Create a new Currency Conversion Quote using the bunq API.

    This endpoint processes conversion quote requests by validating the data
    and creating a quote through the bunq Currency Conversion Quote API.
    """
    quote_id = CurrencyConversionQuoteApiObject.create(
        amount=AmountObject(quote.amount.value, quote.amount.currency),
        currency_source=quote.currency_source,
        currency_target=quote.currency_target,
        order_type=quote.order_type,
        counterparty_alias=PointerObject(
            quote.counterparty.type, quote.counterparty.value, quote.counterparty.name
        ),
        monetary_account_id=monetary_account_id,
    ).value

    return {
        "message": "Currency conversion quote created successfully",
        "quote_id": quote_id,
    }


@router.get("/quotes/{quote_id}")
@handle_exceptions
async def get_currency_conversion_quote(
    quote_id: int, monetary_account_id: Optional[int] = None
):
    """
    Retrieve a Currency Conversion Quote using the bunq API.

    This endpoint fetches conversion quote details by validating the quote ID
    and monetary account ID.
    """
    quote = CurrencyConversionQuoteApiObject.get(
        currency_conversion_quote_id=quote_id, monetary_account_id=monetary_account_id
    ).value

    return {
        "message": "Currency conversion quote retrieved successfully",
        "quote": quote,
    }


@router.put("/quotes/{quote_id}")
@handle_exceptions
async def update_currency_conversion_quote(
    quote_id: int,
    update: CurrencyConversionQuoteStatusUpdate,
    monetary_account_id: Optional[int] = None,
):
    """
    Update a Currency Conversion Quote's status using the bunq API.

    This endpoint updates the status of a conversion quote (accept or reject it)
    by validating the quote ID and monetary account ID.
    """
    quote = CurrencyConversionQuoteApiObject.update(
        currency_conversion_quote_id=quote_id,
        status=update.status,
        monetary_account_id=monetary_account_id,
    ).value

    return {
        "message": f"Currency conversion quote status updated to {update.status}",
        "quote": quote,
    }


@router.get("/conversions/{conversion_id}")
@handle_exceptions
async def get_currency_conversion(
    conversion_id: int, monetary_account_id: Optional[int] = None
):
    """
    Retrieve a Currency Conversion using the bunq API.

    This endpoint fetches conversion details by validating the conversion ID
    and monetary account ID.
    """
    conversion = CurrencyConversionApiObject.get(
        currency_conversion_id=conversion_id, monetary_account_id=monetary_account_id
    ).value

    return {
        "message": "Currency conversion retrieved successfully",
        "conversion": conversion,
    }


@router.get("/conversions")
@handle_exceptions
async def list_currency_conversions(monetary_account_id: Optional[int] = None):
    """
    List all currency conversions for a monetary account.

    This endpoint retrieves all currency conversions performed on a given monetary account.
    """
    conversions = CurrencyConversionApiObject.list(
        monetary_account_id=monetary_account_id
    ).value

    return {
        "message": "Currency conversions retrieved successfully",
        "conversions": conversions,
    }
