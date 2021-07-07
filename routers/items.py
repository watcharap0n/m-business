from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class Transaction(BaseModel):
    id: Optional[str] = None
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
    authUser: Optional[dict] = {}
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
