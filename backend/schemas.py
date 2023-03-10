from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True



class SentimentBase(BaseModel):
    subreddit: str
    topic: str

class SentimentCreate(SentimentBase):
    body: str
    timestamp: datetime
    sentimentrating: float

class Sentiment(SentimentBase):
    id: int

    class Config:
        orm_mode = True
