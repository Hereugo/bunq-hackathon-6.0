from typing import List, Literal, Optional, Union

from bunq.sdk.model.generated.endpoint import (
    NotificationFilterEmailApiObject,
    NotificationFilterFailureApiObject,
    NotificationFilterPushApiObject,
    NotificationFilterUrlApiObject,
    NotificationFilterUrlMonetaryAccountApiObject,
)
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.handle_route_errors import handle_exceptions

router = APIRouter(prefix="/notification_filters", tags=["notification_filters"])


class NotificationFilterCategory(BaseModel):
    """Model representing a notification filter category."""

    category: str = Field(..., description="The category of the notification")


class NotificationFilterEmail(BaseModel):
    """Model for creating email notification filters."""

    category_filter: List[NotificationFilterCategory] = Field(
        ..., description="Categories to filter on"
    )


class NotificationFilterPush(BaseModel):
    """Model for creating push notification filters."""

    category_filter: List[NotificationFilterCategory] = Field(
        ..., description="Categories to filter on"
    )


class NotificationFilterUrl(BaseModel):
    """Model for creating URL notification filters."""

    category_filter: List[NotificationFilterCategory] = Field(
        ..., description="Categories to filter on"
    )
    notification_target: str = Field(..., description="Target URL for the callback")


class NotificationFilterFailure(BaseModel):
    """Model for creating failure notification filters."""

    category_filter: List[NotificationFilterCategory] = Field(
        ..., description="Categories to filter on"
    )
    notification_target: str = Field(..., description="Target URL for the callback")


@router.post("/email")
@handle_exceptions
async def create_email_notification_filter(filter: NotificationFilterEmail):
    """
    Create a new email notification filter using the bunq API.

    This endpoint processes email notification filter requests by validating
    the data and creating a filter through the bunq Notification Filter Email API.
    """
    categories = [category.category for category in filter.category_filter]

    filter_id = NotificationFilterEmailApiObject.create(
        category_filter=categories
    ).value

    return {
        "message": "Email notification filter created successfully",
        "filter_id": filter_id,
    }


@router.get("/email")
@handle_exceptions
async def list_email_notification_filters():
    """
    List all email notification filters.

    This endpoint retrieves all email notification filters.
    """
    filters = NotificationFilterEmailApiObject.list().value

    return {
        "message": "Email notification filters retrieved successfully",
        "filters": filters,
    }


@router.post("/push")
@handle_exceptions
async def create_push_notification_filter(filter: NotificationFilterPush):
    """
    Create a new push notification filter using the bunq API.

    This endpoint processes push notification filter requests by validating
    the data and creating a filter through the bunq Notification Filter Push API.
    """
    categories = [category.category for category in filter.category_filter]

    filter_id = NotificationFilterPushApiObject.create(category_filter=categories).value

    return {
        "message": "Push notification filter created successfully",
        "filter_id": filter_id,
    }


@router.get("/push")
@handle_exceptions
async def list_push_notification_filters():
    """
    List all push notification filters.

    This endpoint retrieves all push notification filters.
    """
    filters = NotificationFilterPushApiObject.list().value

    return {
        "message": "Push notification filters retrieved successfully",
        "filters": filters,
    }


@router.post("/url")
@handle_exceptions
async def create_url_notification_filter(filter: NotificationFilterUrl):
    """
    Create a new URL notification filter using the bunq API.

    This endpoint processes URL notification filter requests by validating
    the data and creating a filter through the bunq Notification Filter URL API.
    """
    categories = [category.category for category in filter.category_filter]

    filter_id = NotificationFilterUrlApiObject.create(
        category_filter=categories, notification_target=filter.notification_target
    ).value

    return {
        "message": "URL notification filter created successfully",
        "filter_id": filter_id,
    }


@router.get("/url")
@handle_exceptions
async def list_url_notification_filters():
    """
    List all URL notification filters.

    This endpoint retrieves all URL notification filters.
    """
    filters = NotificationFilterUrlApiObject.list().value

    return {
        "message": "URL notification filters retrieved successfully",
        "filters": filters,
    }


@router.post("/url/monetary-account/{monetary_account_id}")
@handle_exceptions
async def create_url_monetary_account_notification_filter(
    filter: NotificationFilterUrl, monetary_account_id: int
):
    """
    Create a new URL notification filter for a specific monetary account using the bunq API.

    This endpoint processes URL notification filter requests by validating
    the data and creating a filter through the bunq Notification Filter URL Monetary Account API.
    """
    categories = [category.category for category in filter.category_filter]

    filter_id = NotificationFilterUrlMonetaryAccountApiObject.create(
        category_filter=categories,
        notification_target=filter.notification_target,
        monetary_account_id=monetary_account_id,
    ).value

    return {
        "message": "URL notification filter for monetary account created successfully",
        "filter_id": filter_id,
    }


@router.get("/url/monetary-account/{monetary_account_id}")
@handle_exceptions
async def list_url_monetary_account_notification_filters(monetary_account_id: int):
    """
    List all URL notification filters for a specific monetary account.

    This endpoint retrieves all URL notification filters for a monetary account.
    """
    filters = NotificationFilterUrlMonetaryAccountApiObject.list(
        monetary_account_id=monetary_account_id
    ).value

    return {
        "message": "URL notification filters for monetary account retrieved successfully",
        "filters": filters,
    }


@router.post("/failure")
@handle_exceptions
async def create_failure_notification_filter(filter: NotificationFilterFailure):
    """
    Create a new failure notification filter using the bunq API.

    This endpoint processes failure notification filter requests by validating
    the data and creating a filter through the bunq Notification Filter Failure API.
    """
    categories = [category.category for category in filter.category_filter]

    filter_id = NotificationFilterFailureApiObject.create(
        category_filter=categories, notification_target=filter.notification_target
    ).value

    return {
        "message": "Failure notification filter created successfully",
        "filter_id": filter_id,
    }


@router.get("/failure")
@handle_exceptions
async def list_failure_notification_filters():
    """
    List all failure notification filters.

    This endpoint retrieves all failure notification filters.
    """
    filters = NotificationFilterFailureApiObject.list().value

    return {
        "message": "Failure notification filters retrieved successfully",
        "filters": filters,
    }
