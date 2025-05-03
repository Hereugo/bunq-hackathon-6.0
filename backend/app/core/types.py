from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Amount(BaseModel):
    """Model representing a monetary amount with currency."""

    value: str = Field(
        default="10.00", description="The amount value as a string (e.g. '10.00')"
    )
    currency: str = Field(
        default="EUR",
        description="The currency code (e.g. 'EUR')",
        min_length=3,
        max_length=3,
    )

    @field_validator("value")
    def validate_amount_format(cls, v):
        """Validate that the amount is in correct format."""
        try:
            # Check if the value can be converted to float
            float_val = float(v)
            if float_val <= 0:
                raise ValueError("Amount must be positive")

            # Check if it has correct decimal format
            if "." in v and len(v.split(".")[1]) > 2:
                raise ValueError("Amount can have maximum of 2 decimal places")

            return v
        except ValueError as e:
            raise ValueError(f"Invalid amount format: {str(e)}")


class CounterpartyPointer(BaseModel):
    """Model representing a counterparty (recipient) identification."""

    type: Literal["EMAIL", "PHONE_NUMBER", "IBAN"] = Field(
        ..., description="Type of pointer to identify the counterparty"
    )
    value: str = Field(
        default="sugardaddy@bunq.com",
        description="Value of the pointer (email, phone number, or IBAN)",
    )
    name: str = Field(
        default="Sugar Daddy", description="Name of the counterparty (recipient)"
    )

    @field_validator("value")
    def set_default_value_by_type(cls, v, info):
        """Set default value based on type if not provided"""
        if not v and info.data.get("type") == "EMAIL":
            return "sugardaddy@bunq.com"
        return v
