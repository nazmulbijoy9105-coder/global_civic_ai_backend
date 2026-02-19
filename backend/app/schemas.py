from pydantic import BaseModel
from typing import Optional


# --- User Schemas ---

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


# --- Token Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# --- Question Schemas ---

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True


# --- Response Schemas ---

class ResponseBase(BaseModel):
    user_id: int
    question_id: int
    answer: str

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int

    class Config:
        from_attributes = True


# --- Payment Schemas ---

class PaymentCreate(BaseModel):
    user_id: int
    amount: float
    provider: str

class PaymentOut(BaseModel):
    id: int
    user_id: int
    amount: float
    provider: str
    status: str

    class Config:
        from_attributes = True