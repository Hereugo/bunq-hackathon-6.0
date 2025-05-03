import functools

from bunq.sdk.exception.bad_request_exception import BadRequestException
from bunq.sdk.exception.forbidden_exception import ForbiddenException
from bunq.sdk.exception.method_not_allowed_exception import MethodNotAllowedException
from bunq.sdk.exception.not_found_exception import NotFoundException
from bunq.sdk.exception.please_contact_bunq_exception import PleaseContactBunqException
from bunq.sdk.exception.too_many_requests_exception import TooManyRequestsException
from bunq.sdk.exception.unauthorized_exception import UnauthorizedException
from bunq.sdk.exception.unknown_api_error_exception import UnknownApiErrorException
from fastapi import HTTPException, status


def handle_exceptions(func):
    """
    Decorator to handle exceptions in API routes.
    Catches any exceptions and returns an appropriate HTTP error response.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            try:
                return await func(*args, **kwargs)
            except BadRequestException as e:
                # Status code 400
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Bad Request: {e.message if e.message else str(e)}"
                )
            except UnauthorizedException as e:
                # Status code 401
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Unauthorized: {e.message if e.message else str(e)}",
                )
            except ForbiddenException as e:
                # Status code 403
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Forbidden: {e.message if e.message else str(e)}"
                )
            except NotFoundException as e:
                # Status code 404
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Not Found: {e.message if e.message else str(e)}"
                )
            except MethodNotAllowedException as e:
                # Status code 405
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method Not Allowed: {e.message if e.message else str(e)}",
                )
            except TooManyRequestsException as e:
                # Status code 429
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Too Many Requests: {e.message if e.message else str(e)}",
                )
            except PleaseContactBunqException as e:
                # Status code 500 - with specific message to contact bunq support
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal Server Error: Please contact bunq support via the support chat in the bunq app.",
                )
            except UnknownApiErrorException as e:
                # Fallback for any other bunq API errors
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unknown API Error: {e.message if e.message else str(e)}",
                )
            except Exception as e:
                # General exception handler for any other exceptions
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error: {e.message if e.message else str(e)}",
                )
        except Exception as e:
            # Catch-all for any unhandled exceptions

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error, handle exceptions failed: {str(e)}",
            )

    return wrapper
