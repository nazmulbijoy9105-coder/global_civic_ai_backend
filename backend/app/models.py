from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    has_paid = Column(Boolean, default=False)

    payments = relationship("PaymentHistory", back_populates="user")

class PaymentHistory(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String, nullable=False)   # e.g., Stripe, PayPal, Razorpay
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)     # success, failed, pending
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")