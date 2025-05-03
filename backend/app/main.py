import logging
import os
from pathlib import Path

from app.router.general import general_router
from bunq import ApiEnvironmentType, Pagination
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import (
    DraftPaymentApiObject,
    MonetaryAccountBankApiObject,
    UserApiObject,
)
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

load_dotenv()

BUNQ_USER_API_KEY = os.getenv("BUNQ_USER_API_KEY", "")
BUNQ_CONF_DIR = Path(os.getenv("BUNQ_CONF_DIR", "conf")).resolve()
BUNQ_CONF_PATH = BUNQ_CONF_DIR / os.getenv("BUNQ_CONF_FILE", "bunq_api_context.conf")

if not os.path.exists(BUNQ_CONF_DIR):
    os.makedirs(BUNQ_CONF_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
app = FastAPI(root_path="/backend")
pagination = Pagination()
pagination.count = 10

# Register routers
app.include_router(general_router)


@app.middleware("http")
async def load_or_create_api_context(request: Request, call_next):
    """Create or restore api context"""

    if not os.path.isfile(BUNQ_CONF_PATH):
        create_user_session()

    api_context = ApiContext.restore(str(BUNQ_CONF_PATH))
    BunqContext.load_api_context(api_context)

    response = await call_next(request)
    return response


@app.get("/create_user_session")
def create_user_session():
    """Create a bunq user session."""
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        BUNQ_USER_API_KEY,
        "LLM Agent",
    )
    api_context.save(str(BUNQ_CONF_PATH))
    return Response(status_code=200)


@app.get("/user")
def get_user(request: Request):
    response = UserApiObject.get()
    return response


@app.get("/monetary_account")
def get_monetary_account(request: Request):
    user_context = BunqContext.user_context()

    # Get the user ID
    primary_account = user_context.primary_monetary_account
    response = MonetaryAccountBankApiObject.get(primary_account.id_)
    return response
