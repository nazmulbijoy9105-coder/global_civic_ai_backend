from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

def get_utc_now():
    """Returns the current UTC time."""
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user") # Matches auth.py logic
    created_at = Column(DateTime, default=get_utc_now)
    is_admin = Column(Boolean, default=False)
    has_paid = Column(Boolean, default=False)

    responses = relationship("Response", back_populates="user")
    payments = relationship("PaymentHistory", back_populates="user")
    sessions = relationship("AssessmentSession", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, default="general")
    age_group = Column(String, nullable=True)
    text_en = Column(Text, nullable=False)
    text_bn = Column(Text, nullable=True)
    text_hi = Column(Text, nullable=True)
    text_jp = Column(Text, nullable=True)
    text_cn = Column(Text, nullable=True)
    options = Column(String, nullable=True, default="Always,Sometimes,Rarely,Never")

    responses = relationship("Response", back_populates="question")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=True)
    trait = Column(String, nullable=True) # Essential for scoring logic
    answer = Column(String, nullable=True)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=get_utc_now)

    user = relationship("User", back_populates="responses")
    question = relationship("Question", back_populates="responses")


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="in_progress")
    current_index = Column(Integer, default=0)
    total_questions = Column(Integer, default=20)
    created_at = Column(DateTime, default=get_utc_now)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")
    scores = relationship("AdaptiveScore", back_populates="session")
    audit_logs = relationship("AuditLog", back_populates="session")


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="completed")
    payment_method = Column(String, default="card")
    timestamp = Column(DateTime, default=get_utc_now)

    user = relationship("User", back_populates="payments")


class AdaptiveScore(Base):
    __tablename__ = "adaptive_scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    trait = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)

    session = relationship("AssessmentSession", back_populates="scores")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    trait = Column(String, nullable=False)
    factor = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    session = relationship("AssessmentSession", back_populates="audit_logs")