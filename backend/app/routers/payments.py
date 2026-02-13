from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import PaymentHistory

router = APIRouter()

@router.post("/create")
def create_payment(user_id: int, amount: int, provider: str, db: Session = Depends(get_db)):
    payment = PaymentHistory(
        user_id=user_id,
        amount=amount,
        provider=provider,
        status="pending"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return {"status": "success", "payment_id": payment.id, "amount": amount}

@router.get("/history/{user_id}")
def payment_history(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(PaymentHistory).filter(PaymentHistory.user_id == user_id).all()
    return payments
