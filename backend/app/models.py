from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    locale = Column(String(10))
    has_paid = Column(Boolean, default=False)
    payments = relationship("PaymentHistory", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class PaymentHistory(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String(50))
    amount = Column(Integer)
    status = Column(String(50))
    timestamp = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="payments")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    details = Column(Text)
    user = relationship("User", back_populates="audit_logs")
