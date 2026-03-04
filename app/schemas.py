from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_admin: bool
    has_paid: bool

    class Config:
        from_attributes = True


class QuestionOut(BaseModel):
    id: int
    category: str
    age_group: Optional[str] = None
    text_en: str
    text_bn: Optional[str] = None
    text_hi: Optional[str] = None
    text_jp: Optional[str] = None
    text_cn: Optional[str] = None
    options: Optional[str] = "Always,Sometimes,Rarely,Never"

    class Config:
        from_attributes = True


class ResponseCreate(BaseModel):
    question_id: int
    answer: Optional[str] = None
    score: float


class ResponseOut(BaseModel):
    id: int
    user_id: int
    question_id: int
    session_id: Optional[int] = None
    answer: Optional[str] = None
    score: float
    created_at: datetime

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    total_questions: int = 20


class SessionOut(BaseModel):
    id: int
    user_id: int
    status: str
    current_index: int
    total_questions: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    amount: float
    currency: str = "USD"
    payment_method: str = "card"


class PaymentHistoryOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    status: str
    payment_method: str
    timestamp: datetime

    class Config:
        from_attributes = True


class AdaptiveScoreOut(BaseModel):
    id: int
    session_id: int
    trait: str
    score: float
    confidence: float

    class Config:
        from_attributes = True


class AuditLogOut(BaseModel):
    id: int
    session_id: int
    trait: str
    factor: str
    value: float

    class Config:
        from_attributes = True


class ReportOut(BaseModel):
    session_id: int
    user_id: int
    scores: dict
    summary: str
    recommendations: list[str]
    created_at: datetime
