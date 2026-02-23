from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

# ✅ User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    has_paid = Column(Boolean, default=False)

    responses = relationship("Response", back_populates="user")
    payments = relationship("PaymentHistory", back_populates="user")
    sessions = relationship("Session", back_populates="user")

# ✅ Payment history
class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")

# ✅ Question bank
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    trait = Column(String, index=True)
    text = Column(Text, nullable=False)
    weight = Column(Float, default=1.0)

    responses = relationship("Response", back_populates="question")

# ✅ User responses
class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="responses")
    question = relationship("Question", back_populates="responses")

# ✅ Assessment session
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")
    scores = relationship("AdaptiveScore", back_populates="session")
    audits = relationship("AuditLog", back_populates="session")

# ✅ Adaptive scores
class AdaptiveScore(Base):
    __tablename__ = "adaptive_scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    trait = Column(String, index=True)
    score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)

    session = relationship("Session", back_populates="scores")

# ✅ Responsible AI audit logs
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    trait = Column(String, index=True)
    factor = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    session = relationship("Session", back_populates="audits")