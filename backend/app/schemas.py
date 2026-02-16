from pydantic import BaseModel

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class ResponseBase(BaseModel):
    user_id: int
    question_id: int
    answer: str

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int

    class Config:
        orm_mode = True