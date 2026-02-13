from pydantic import BaseModel

class Question(BaseModel):
    id: int
    category: str
    age_group: str
    question_en: str
    question_bn: str
    question_hi: str
    question_jp: str
    question_cn: str
    options: str

class Payment(BaseModel):
    user_id: str
    amount: float
    currency: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
