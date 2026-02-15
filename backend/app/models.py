from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # roles: user, admin, institution
    locale = Column(String(10))
    has_paid = Column(Boolean, default=False)

    # Relationships
    payments = relationship("PaymentHistory", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class PaymentHistory(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String(50))  # e.g., Stripe, Razorpay, bKash
    amount = Column(Integer)
    status = Column(String(50))    # e.g., success, failed, pending
    timestamp = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)  # e.g., login, payment, role_change
    timestamp = Column(DateTime, server_default=func.now())
    details = Column(Text)  # optional extra info

    # Relationships
    user = relationship("User", back_populates="audit_logs")