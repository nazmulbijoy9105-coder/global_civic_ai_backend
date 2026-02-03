# Pydantic models placeholder
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
