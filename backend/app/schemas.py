from pydantic import BaseModel, EmailStr
from datetime import datetime

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
    email: EmailStr
    created_at: datetime
    is_admin: bool
    has_paid: bool

    class Config:
        orm_mode = True

class QuestionOut(BaseModel):
    id: int
    text: str
    class Config:
        orm_mode = True

class ResponseCreate(BaseModel):
    user_id: int
    trait: str
    question_id: int
    score: float

class ResponseOut(BaseModel):
    id: int
    user_id: int
    question_id: int
    score: float
    class Config:
        orm_mode = True

class SessionOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class PaymentHistoryOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    timestamp: datetime
    class Config:
        orm_mode = True

class AdaptiveScoreOut(BaseModel):
    id: int
    session_id: int
    trait: str
    score: float
    confidence: float
    class Config:
        orm_mode = True

class AuditLogOut(BaseModel):
    id: int
    session_id: int
    trait: str
    factor: str
    value: float
    class Config:
        orm_mode = True