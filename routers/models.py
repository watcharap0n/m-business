from pydantic import BaseModel, Field
from typing import Optional, List, Dict

CUSTOMER = 'CUSTOMER'


class Transaction(BaseModel):
    id: Optional[str] = Field(None, example='id MongoDb (string)')
    name: Optional[str] = Field(None, example=f'{CUSTOMER} Name (string)')
    email: Optional[str] = Field(None, example=f'{CUSTOMER} Email (string)')
    company: Optional[str] = Field(None, example=f'{CUSTOMER} Company (string)')
    tel: Optional[str] = Field(None, example=f'{CUSTOMER} number phone (string)')
    product: Optional[str] = Field(None, example=f'{CUSTOMER} Product (string)')
    other: Optional[str] = Field(None, example=f'{CUSTOMER} Other Product (string)')
    message: Optional[str] = Field(None, example=f'{CUSTOMER} Description message')
    userId: Optional[str] = Field(None, example='Token user id LINE or Facebook')
    email_private: Optional[str] = Field(None, example='email private Customer')
    profile: Optional[str] = Field(None, example='Profile LINE or Facebook')
    picture: Optional[str] = Field(None, example='Picture LINE or Facebook')
    channel: Optional[str] = Field(None, example='Get Channel LINE or Facebook')
    username: Optional[str] = None
    uid: Optional[str] = None
    tag: Optional[list] = []
    date: Optional[str] = None
    time: Optional[str] = None


class FROM_MANGO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    tel: Optional[str] = None
    product: Optional[str] = None
    other: Optional[str] = None
    message: Optional[str] = None
    userId: Optional[str] = None
    email_private: Optional[str] = None
    profile: Optional[str] = None
    picture: Optional[str] = None
    channel: Optional[str] = None


class TokenLINE(BaseModel):
    ACCESS_TOKEN: Optional[str] = None
    SECRET_LINE: Optional[str] = None


class INTENT_BOT(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    question: Optional[list] = None
    answer: Optional[list] = None
    uid: Optional[str] = None
    access_token: Optional[str] = None


class UserItem(BaseModel):
    type: str
    description: Optional[str] = None
