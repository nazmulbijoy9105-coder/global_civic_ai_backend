from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# --- AUTH SCHEMAS ---

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str = "user"
    is_admin: bool = False
    has_paid: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- ASSESSMENT SCHEMAS ---

class QuestionOut(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)

class ResponseCreate(BaseModel):
    user_id: int
    trait: str
    question_id: int
    score: float

class ResponseOut(BaseModel):
    id: int
    user_id: int
    question_id: int
    trait: str
    score: float

    model_config = ConfigDict(from_attributes=True)

class SessionOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- ANALYTICS & PAYMENTS ---

class PaymentHistoryOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class AdaptiveScoreOut(BaseModel):
    id: int
    session_id: int
    trait: str
    score: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class AuditLogOut(BaseModel):
    id: int
    session_id: int
    trait: str
    factor: str
    value: float

    model_config = ConfigDict(from_attributes=True)