from types import NoneType
from typing import List, Literal, Optional

from app.core.handle_route_errors import handle_exceptions
from app.core.types import Amount
from bunq.sdk.model.generated.endpoint import (
    MonetaryAccountApiObject,
    MonetaryAccountBankApiObject,
    MonetaryAccountCardApiObject,
    MonetaryAccountExternalApiObject,
    MonetaryAccountExternalSavingsApiObject,
    MonetaryAccountJointApiObject,
    MonetaryAccountSavingsApiObject,
)
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/monetary-accounts", tags=["monetary_accounts"])


MonetaryAccountStatus = Literal["ACTIVE", "BLOCKED", "CANCELLED"]
MonetaryAccountSubStatus = Literal[
    "NONE",
    "PENDING_REOPEN",
    "COMPLETELY",
    "ONLY_ACCEPTING_INCOMING",
    "REDEMPTION_INVOLUNTARY",
    "REDEMPTION_VOLUNTARY",
    "PERMANENT",
]


class MonetaryAccountSetting(BaseModel):
    """Model representing monetary account settings."""

    color: Optional[str] = Field(
        None,
        description="The color chosen for the monetary account in hexadecimal format",
    )
    icon: Optional[str] = Field(
        None, description="The icon chosen for the monetary account"
    )
    default_avatar_status: Optional[str] = Field(
        default="AVATAR_DEFUALT", description="The status of the avatar"
    )
    restriction_chat: Optional[Literal["ALLOW_INCOMING", "BLOCK_INCOMING"]] = Field(
        None,
        description="The chat restriction. Possible values are ALLOW_INCOMING or BLOCK_INCOMING",
    )


class CreateMonetaryAccountBank(BaseModel):
    """Model for creating a new monetary account bank."""

    currency: str = Field(
        default="EUR",
        description="The currency of the monetary account",
        min_length=3,
        max_length=3,
    )
    description: str = Field(
        ..., description="The description of the monetary account", max_length=140
    )
    daily_limit: Amount = Field(
        default=Amount(value="1000.00", currency="EUR"),
        description="The daily spending limit",
    )
    status: MonetaryAccountStatus = Field(
        default="ACTIVE",
        description="The status of the monetary account",
    )
    sub_status: MonetaryAccountSubStatus = Field(
        default="NONE",
        description="The sub-status of the MonetaryAccountBank providing extra information regarding the status. Will be NONE for ACTIVE or PENDING_REOPEN, COMPLETELY or ONLY_ACCEPTING_INCOMING for BLOCKED and REDEMPTION_INVOLUNTARY, REDEMPTION_VOLUNTARY or PERMANENT for CANCELLED.",
    )
    reason: Optional[str] = Field(
        default="OTHER",
        description="The reason for voluntarily cancelling (closing) the MonetaryAccountBack, can onlly be OTHER",
    )
    reason_description: Optional[str] = Field(
        default="this is a description",
        description="The optional free-form reason for voluntarily cancelling (closing) the MonetaryAccountBank. Can be any user provided message.",
    )
    display_name: str = Field(
        default="M. Rozemeijer",
        description="The legal name of the user / company using this monetary account.",
    )
    setting: Optional[MonetaryAccountSetting] = Field(
        None, description="The settings of the monetary account"
    )
    country_iban: Optional[str] = Field(
        default="NL",
        description="The country of the monetary account IBAN.",
    )


class UpdateMonetaryAccountBankStatus(BaseModel):
    status: MonetaryAccountStatus = Field(
        default="ACTIVE",
        description="The status of the monetary account",
    )
    sub_status: MonetaryAccountSubStatus = Field(
        default="NONE",
        description="The sub-status of the MonetaryAccountBank providing extra information regarding the status. Will be NONE for ACTIVE or PENDING_REOPEN, COMPLETELY or ONLY_ACCEPTING_INCOMING for BLOCKED and REDEMPTION_INVOLUNTARY, REDEMPTION_VOLUNTARY or PERMANENT for CANCELLED.",
    )


class UpdateMonetaryAccountBankData(BaseModel):
    currency: str = Field(
        default="EUR",
        description="The currency of the monetary account",
        min_length=3,
        max_length=3,
    )
    description: str = Field(
        ..., description="The description of the monetary account", max_length=140
    )
    daily_limit: Amount = Field(
        default=Amount(value="1000.00", currency="EUR"),
        description="The daily spending limit",
    )
    reason: Optional[str] = Field(
        default="OTHER",
        description="The reason for voluntarily cancelling (closing) the MonetaryAccountBack, can onlly be OTHER",
    )
    reason_description: Optional[str] = Field(
        default="this is a description",
        description="The optional free-form reason for voluntarily cancelling (closing) the MonetaryAccountBank. Can be any user provided message.",
    )
    display_name: str = Field(
        default="M. Rozemeijer",
        description="The legal name of the user / company using this monetary account.",
    )
    setting: Optional[MonetaryAccountSetting] = Field(
        None, description="The settings of the monetary account"
    )


class CreateMonetaryAccountJoint(BaseModel):
    """Model for creating a new joint monetary account."""

    currency: str = Field(
        default="EUR",
        description="The currency of the monetary account",
        min_length=3,
        max_length=3,
    )
    description: str = Field(
        default="this is a description",
        description="The description of the monetary account",
        max_length=140,
    )
    daily_limit: Amount = Field(
        default=Amount(value="1000.00", currency="EUR"),
        description="The daily spending limit",
    )
    overdraft_limit: Amount = Field(
        default=Amount(value="2000.00", currency="EUR"),
        description="The maximum Amount the MonetaryACccountJoint can be in 'the red'",
    )
    status: MonetaryAccountStatus = Field(
        default="ACTIVE",
        description="The status of the monetary account",
    )
    sub_status: MonetaryAccountSubStatus = Field(
        default="NONE",
        description="The sub-status of the MonetaryAccountBank providing extra information regarding the status. Will be NONE for ACTIVE or PENDING_REOPEN, COMPLETELY or ONLY_ACCEPTING_INCOMING for BLOCKED and REDEMPTION_INVOLUNTARY, REDEMPTION_VOLUNTARY or PERMANENT for CANCELLED.",
    )
    reason: Optional[str] = Field(
        default="OTHER",
        description="The reason for voluntarily cancelling (closing) the MonetaryAccountBack, can onlly be OTHER",
    )
    reason_description: Optional[str] = Field(
        default="this is a description",
        description="The optional free-form reason for voluntarily cancelling (closing) the MonetaryAccountBank. Can be any user provided message.",
    )
    setting: Optional[MonetaryAccountSetting] = Field(
        None, description="The settings of the monetary account"
    )
    all_co_owner: List[str] = Field(
        ..., description="The email addresses of the co-owners"
    )
    alias: List[str] = None
    avatar_uuid: NoneType = None


class CreateMonetaryAccountExternal(BaseModel):
    """Model for creating a new external monetary account."""

    description: str = Field(
        ..., description="The description of the monetary account", max_length=140
    )
    setting: Optional[MonetaryAccountSetting] = Field(
        None, description="The settings of the monetary account"
    )
    status: Optional[MonetaryAccountStatus] = Field(
        None, description="The status of the monetary account"
    )
    alias: str = Field(..., description="The alias for the external account")


class UpdateMonetaryAccountExternal(BaseModel):
    """Model for updating an external monetary account."""

    description: Optional[str] = Field(
        None, description="The description of the monetary account", max_length=140
    )
    setting: Optional[MonetaryAccountSetting] = Field(
        None, description="The settings of the monetary account"
    )
    status: Optional[MonetaryAccountStatus] = Field(
        None, description="The status of the monetary account"
    )


class CreateMonetaryAccountSavings(BaseModel):
    """Model for creating a new savings monetary account."""

    currency: str = Field(
        default="EUR",
        description="The currency of the monetary account",
        min_length=3,
        max_length=3,
    )
    description: str = Field(
        ..., description="The description of the monetary account", max_length=140
    )
    daily_limit: Amount = Field(
        default=Amount(value="1000.00", currency="EUR"),
        description="The daily spending limit",
    )
    setting: Optional[MonetaryAccountSetting] = Field(
        None, description="The settings of the monetary account"
    )
    status: Optional[MonetaryAccountStatus] = Field(
        None, description="The status of the monetary account"
    )


# Generic Monetary Account endpoints
@router.get("/")
@handle_exceptions
async def list_monetary_accounts():
    """
    List all monetary accounts.

    This endpoint retrieves all monetary accounts.
    """
    accounts = MonetaryAccountApiObject.list().value

    return {"message": "Monetary accounts retrieved successfully", "accounts": accounts}


# Bank Monetary Account endpoints
@router.post("/bank")
@handle_exceptions
async def create_monetary_account_bank(account: CreateMonetaryAccountBank):
    """
    Create a new monetary account bank using the bunq API.

    This endpoint processes monetary account bank creation requests.
    """
    daily_limit = Amount(
        value=account.daily_limit.value,
        currency=account.daily_limit.currency,
    )

    # Convert setting to dict if provided
    setting_dict = None
    if account.setting:
        setting_dict = {}
        if account.setting.color:
            setting_dict["color"] = account.setting.color
        if account.setting.icon:
            setting_dict["icon"] = account.setting.icon
        if account.setting.default_avatar_status:
            setting_dict["default_avatar_status"] = (
                account.setting.default_avatar_status
            )

    account_id = MonetaryAccountBankApiObject.create(
        currency=account.currency,
        description=account.description,
        daily_limit=daily_limit,
        status=account.status,
        sub_status=account.sub_status,
        reason=account.reason,
        reason_description=account.reason_description,
        display_name=account.display_name,
        setting=setting_dict,
        country_iban=account.country_iban,
    ).value

    return {
        "message": "Monetary account bank created successfully",
        "account_id": account_id,
    }


@router.get("/bank")
@handle_exceptions
async def list_monetary_account_banks():
    """
    List all monetary account banks.

    This endpoint retrieves all monetary account banks.
    """
    accounts = MonetaryAccountBankApiObject.list().value

    return {
        "message": "Monetary account banks retrieved successfully",
        "accounts": accounts,
    }


@router.get("/bank/{account_id}")
@handle_exceptions
async def get_monetary_account_bank(account_id: int):
    """
    Retrieve a monetary account bank using the bunq API.

    This endpoint fetches monetary account bank details by account ID.
    """
    account = MonetaryAccountBankApiObject.get(
        monetary_account_bank_id=account_id
    ).value

    return {
        "message": "Monetary account bank retrieved successfully",
        "account": account,
    }


@router.put("/bank/data/{account_id}", deprecated=True)
@handle_exceptions
async def update_monetary_account_bank_data(
    account_id: int, account: UpdateMonetaryAccountBankData
):
    """
    Update a monetary account bank using the bunq API.

    This endpoint processes monetary account bank update requests.
    """
    # Convert setting to dict if provided
    setting_dict = None
    if account.setting:
        setting_dict = {}
        if account.setting.color:
            setting_dict["color"] = account.setting.color
        if account.setting.icon:
            setting_dict["icon"] = account.setting.icon
        if account.setting.default_avatar_status:
            setting_dict["default_avatar_status"] = (
                account.setting.default_avatar_status
            )

    updated_id = MonetaryAccountBankApiObject.update(
        monetary_account_bank_id=account_id,
        description=account.description,
        daily_limit=account.daily_limit,
        reason=account.reason,
        reason_description=account.reason_description,
        display_name=account.display_name,
        setting=setting_dict,
    ).value

    return {
        "message": "Monetary account bank updated successfully",
        "account_id": updated_id,
    }


@router.put("/bank/status/{account_id}", deprecated=True)
@handle_exceptions
async def update_monetary_account_bank_status(
    account_id: int, account: UpdateMonetaryAccountBankStatus
):
    """
    Update a monetary account bank using the bunq API.

    This endpoint processes monetary account bank update requests.
    """
    updated_id = MonetaryAccountBankApiObject.update(
        monetary_account_bank_id=account_id,
        status=account.status,
        sub_status=account.sub_status,
    ).value

    return {
        "message": "Monetary account bank updated successfully",
        "account_id": updated_id,
    }


# Joint Monetary Account endpoints
@router.post("/joint", deprecated=True)
@handle_exceptions
async def create_monetary_account_joint(account: CreateMonetaryAccountJoint):
    """
    Create a new joint monetary account using the bunq API.

    This endpoint processes joint monetary account creation requests.
    """

    # Convert setting to dict if provided
    setting_dict = None
    if account.setting:
        setting_dict = {}
        if account.setting.color:
            setting_dict["color"] = account.setting.color
        if account.setting.icon:
            setting_dict["icon"] = account.setting.icon
        if account.setting.default_avatar_status:
            setting_dict["default_avatar_status"] = (
                account.setting.default_avatar_status
            )

    account_id = MonetaryAccountJointApiObject.create(
        currency=account.currency,
        all_co_owner=account.all_co_owner,
        description=account.description,
        daily_limit=account.daily_limit,
        overdraft_limit=account.overdraft_limit,
        alias=account.alias,
        avatar_uuid=account.avatar_uuid,
        status=account.status,
        sub_status=account.sub_status,
        reason=account.reason,
        reason_description=account.reason_description,
        setting=setting_dict,
    ).value

    return {
        "message": "Joint monetary account created successfully",
        "account_id": account_id,
    }


@router.get("/joint")
@handle_exceptions
async def list_monetary_account_joints():
    """
    List all joint monetary accounts.

    This endpoint retrieves all joint monetary accounts.
    """
    accounts = MonetaryAccountJointApiObject.list().value

    return {
        "message": "Joint monetary accounts retrieved successfully",
        "accounts": accounts,
    }


@router.get("/joint/{account_id}")
@handle_exceptions
async def get_monetary_account_joint(account_id: int):
    """
    Retrieve a joint monetary account using the bunq API.

    This endpoint fetches joint monetary account details by account ID.
    """
    account = MonetaryAccountJointApiObject.get(
        monetary_account_joint_id=account_id
    ).value

    return {
        "message": "Joint monetary account retrieved successfully",
        "account": account,
    }


@router.get("/card")
@handle_exceptions
async def list_monetary_account_cards():
    """
    List all card monetary accounts.

    This endpoint retrieves all card monetary accounts.
    """
    accounts = MonetaryAccountCardApiObject.list().value

    return {
        "message": "Card monetary accounts retrieved successfully",
        "accounts": accounts,
    }


# Card Monetary Account endpoints
@router.get("/card/{account_id}")
@handle_exceptions
async def get_monetary_account_card(account_id: int):
    """
    Retrieve a card monetary account using the bunq API.

    This endpoint fetches card monetary account details by account ID.
    """
    account = MonetaryAccountCardApiObject.get(
        monetary_account_card_id=account_id
    ).value

    return {
        "message": "Card monetary account retrieved successfully",
        "account": account,
    }


# External Monetary Account endpoints
@router.post("/external", deprecated=True)
@handle_exceptions
async def create_monetary_account_external(account: CreateMonetaryAccountExternal):
    """
    Create a new external monetary account using the bunq API.

    This endpoint processes external monetary account creation requests.
    """

    # Convert setting to dict if provided
    setting_dict = None
    if account.setting:
        setting_dict = {}
        if account.setting.color:
            setting_dict["color"] = account.setting.color
        if account.setting.icon:
            setting_dict["icon"] = account.setting.icon
        if account.setting.default_avatar_status:
            setting_dict["default_avatar_status"] = (
                account.setting.default_avatar_status
            )

    account_id = MonetaryAccountExternalApiObject.create(
        currency=account.currency,
        description=account.description,
        status=account.status,
        alias=account.alias,
        setting=setting_dict,
    ).value

    return {
        "message": "External monetary account created successfully",
        "account_id": account_id,
    }


@router.get("/external")
@handle_exceptions
async def list_monetary_account_externals():
    """
    List all external monetary accounts.

    This endpoint retrieves all external monetary accounts.
    """
    accounts = MonetaryAccountExternalApiObject.list().value

    return {
        "message": "External monetary accounts retrieved successfully",
        "accounts": accounts,
    }


@router.get("/external/{account_id}")
@handle_exceptions
async def get_monetary_account_external(account_id: int):
    """
    Retrieve an external monetary account using the bunq API.

    This endpoint fetches external monetary account details by account ID.
    """
    account = MonetaryAccountExternalApiObject.get(
        monetary_account_external_id=account_id
    ).value

    return {
        "message": "External monetary account retrieved successfully",
        "account": account,
    }


# External Savings Monetary Account endpoints
@router.post("/external-savings", deprecated=True)
@handle_exceptions
async def create_monetary_account_external_savings(
    account: CreateMonetaryAccountExternal,
):
    """
    Create a new external savings monetary account using the bunq API.

    This endpoint processes external savings monetary account creation requests.
    """
    status = account.status.status if account.status else "ACTIVE"

    # Convert setting to dict if provided
    setting_dict = None
    if account.setting:
        setting_dict = {}
        if account.setting.color:
            setting_dict["color"] = account.setting.color
        if account.setting.icon:
            setting_dict["icon"] = account.setting.icon
        if account.setting.default_avatar_status:
            setting_dict["default_avatar_status"] = (
                account.setting.default_avatar_status
            )

    account_id = MonetaryAccountExternalSavingsApiObject.create(
        description=account.description,
        setting=setting_dict,
        status=status,
        alias=account.alias,
    ).value

    return {
        "message": "External savings monetary account created successfully",
        "account_id": account_id,
    }


@router.get("/external-savings")
@handle_exceptions
async def list_monetary_account_external_savings():
    """
    List all external savings monetary accounts.

    This endpoint retrieves all external savings monetary accounts.
    """
    accounts = MonetaryAccountExternalSavingsApiObject.list().value

    return {
        "message": "External savings monetary accounts retrieved successfully",
        "accounts": accounts,
    }


@router.get("/external-savings/{account_id}")
@handle_exceptions
async def get_monetary_account_external_savings(account_id: int):
    """
    Retrieve an external savings monetary account using the bunq API.

    This endpoint fetches external savings monetary account details by account ID.
    """
    account = MonetaryAccountExternalSavingsApiObject.get(
        monetary_account_external_savings_id=account_id
    ).value

    return {
        "message": "External savings monetary account retrieved successfully",
        "account": account,
    }


# Savings Monetary Account endpoints
@router.post("/savings", deprecated=True)
@handle_exceptions
async def create_monetary_account_savings(account: CreateMonetaryAccountSavings):
    """
    Create a new savings monetary account using the bunq API.

    This endpoint processes savings monetary account creation requests.
    """
    daily_limit = BunqAmount(account.daily_limit.value, account.daily_limit.currency)
    status = account.status.status if account.status else "ACTIVE"

    # Convert setting to dict if provided
    setting_dict = None
    if account.setting:
        setting_dict = {}
        if account.setting.color:
            setting_dict["color"] = account.setting.color
        if account.setting.icon:
            setting_dict["icon"] = account.setting.icon
        if account.setting.default_avatar_status:
            setting_dict["default_avatar_status"] = (
                account.setting.default_avatar_status
            )

    account_id = MonetaryAccountSavingsApiObject.create(
        currency=account.currency,
        description=account.description,
        daily_limit=daily_limit,
        setting=setting_dict,
        status=status,
    ).value

    return {
        "message": "Savings monetary account created successfully",
        "account_id": account_id,
    }


@router.get("/savings")
@handle_exceptions
async def list_monetary_account_savings():
    """
    List all savings monetary accounts.

    This endpoint retrieves all savings monetary accounts.
    """
    accounts = MonetaryAccountSavingsApiObject.list().value

    return {
        "message": "Savings monetary accounts retrieved successfully",
        "accounts": accounts,
    }


@router.get("/savings/{account_id}")
@handle_exceptions
async def get_monetary_account_savings(account_id: int):
    """
    Retrieve a savings monetary account using the bunq API.

    This endpoint fetches savings monetary account details by account ID.
    """
    account = MonetaryAccountSavingsApiObject.get(
        monetary_account_savings_id=account_id
    ).value

    return {
        "message": "Savings monetary account retrieved successfully",
        "account": account,
    }


@router.get("/{account_id}")
@handle_exceptions
async def get_monetary_account(account_id: int):
    """
    Retrieve a monetary account using the bunq API.

    This endpoint fetches monetary account details by account ID.
    """
    account = MonetaryAccountApiObject.get(monetary_account_id=account_id).value

    return {"message": "Monetary account retrieved successfully", "account": account}
