from fastapi import APIRouter

from ..router.billing_contract_subscription import (
    router as billing_contract_subscription_router,
)
from ..router.cards import router as cards_router
from ..router.currency_conversion import router as currency_conversion_router
from ..router.draft_payments import router as draft_payments_router
from ..router.inquiries import router as inquiries_router
from ..router.monetary_account import router as monetary_account_router
from ..router.notification_filter import router as notification_filter_router
from ..router.payments import router as payments_router
from ..router.schedule_payment import router as schedule_payment_router
from ..router.users import router as user_router

general_router = APIRouter()
general_router.include_router(billing_contract_subscription_router)
general_router.include_router(cards_router)
general_router.include_router(currency_conversion_router)
general_router.include_router(draft_payments_router)
general_router.include_router(inquiries_router)
general_router.include_router(monetary_account_router)
general_router.include_router(notification_filter_router)
general_router.include_router(payments_router)
general_router.include_router(user_router)
general_router.include_router(schedule_payment_router)
