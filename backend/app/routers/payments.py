# Payments router placeholder
from fastapi import APIRouter
from backend.app.models import Payment

router = APIRouter()

@router.post("/create")
def create_payment(payment: Payment):
    return {"status": "success", "amount": payment.amount, "currency": payment.currency}
