from typing import Optional

from bunq.sdk.model.generated.endpoint import UserApiObject
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.core.handle_route_errors import handle_exceptions

router = APIRouter(prefix="/users", tags=["users"])


class UserDetails(BaseModel):
    """Model representing essential user information."""

    id: int = Field(..., description="User ID")
    created: str = Field(...,
                         description="Timestamp when the user was created")
    updated: str = Field(...,
                         description="Timestamp when the user was last updated")
    alias: Optional[dict] = Field(None, description="User alias information")
    avatar: Optional[dict] = Field(None, description="User avatar information")
    status: Optional[str] = Field(None, description="User status")
    sub_status: Optional[str] = Field(None, description="User sub-status")
    display_name: Optional[str] = Field(None, description="User display name")


@router.get("/current")
@handle_exceptions
async def get_current_user():
    """
    Get the currently authenticated user.

    Returns user details from the bunq API for the current user.
    """
    user = UserApiObject.get().value

    return {"message": "Current user retrieved successfully", "user": user}


@router.get("/")
@handle_exceptions
async def list_users(
    limit: int = Query(10, description="Maximum number of users to return")
):
    """
    List all accessible users.

    Returns a list of users available to the authenticated session.
    """
    users = UserApiObject.list().value

    return {"message": "Users retrieved successfully", "users": users}


@router.get("/{user_id}")
@handle_exceptions
async def get_user_by_id(user_id: int):
    """
    Get a specific user by ID.

    Retrieve detailed information about a user by their unique identifier.
    """
    user = UserApiObject.get(user_id).value

    return {"message": "User retrieved successfully", "user_id": user_id, "user": user}
