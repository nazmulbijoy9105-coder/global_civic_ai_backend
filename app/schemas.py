from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

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
    model_config = ConfigDict(from_attributes=True)

class QuestionOut(BaseModel):
    id: int
    category: str
    age_group: Optional[str]
    text_en: str
    text_bn: Optional[str]
    text_hi: Optional[str]
    text_jp: Optional[str]
    text_cn: Optional[str]
    options: str
    model_config = ConfigDict(from_attributes=True)

class ResponseCreate(BaseModel):
    question_id: int
    answer: str
    score: float

class SessionOut(BaseModel):
    id: int
    user_id: int
    status: str
    current_index: int
    total_questions: int
    created_at: datetime
    completed_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
class ResponseOut(BaseModel):
    """Response output schema"""
    id: int
    question_id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
