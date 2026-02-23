from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ✅ User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    is_admin: bool
    has_paid: bool

    class Config:
        orm_mode = True

# ✅ Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ Payment history
class PaymentHistoryOut(BaseModel):
    id: int
    amount: float
    currency: str
    timestamp: datetime

    class Config:
        orm_mode = True

# ✅ Question schemas
class QuestionOut(BaseModel):
    id: int
    trait: str
    text: str
    weight: float

    class Config:
        orm_mode = True

# ✅ Response schemas
class ResponseCreate(BaseModel):
    user_id: int
    question_id: int
    score: float

class ResponseOut(BaseModel):
    id: int
    user_id: int
    question_id: int
    score: float
    timestamp: datetime

    class Config:
        orm_mode = True

# ✅ Session schemas
class SessionOut(BaseModel):
    id: int
    user_id: int
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True

# ✅ Adaptive score schemas
class AdaptiveScoreOut(BaseModel):
    id: int
    session_id: int
    trait: str
    score: float
    confidence: float

    class Config:
        orm_mode = True

# ✅ Audit log schemas
class AuditLogOut(BaseModel):
    id: int
    session_id: int
    trait: str
    factor: str
    value: float

    class Config:
        orm_mode = True