from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class Transaction(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    tel: Optional[str] = None
    product: Optional[str] = None
    company: Optional[str] = None
    channel: Optional[str] = None
    message: Optional[str] = None
    tag: Optional[list] = None


class FROM_MANGO(BaseModel):
    firstname: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    tel: Optional[str] = None
    product: Optional[str] = None
    other: Optional[str] = None
    comment: Optional[str] = None
    userId: Optional[str] = None
    token: Optional[str] = None
    displayName: Optional[str] = None
    picture: Optional[str] = None
    channel: Optional[str] = None


class TokenLINE(BaseModel):
    ACCESS_TOKEN: Optional[str] = None
    SECRET_LINE: Optional[str] = None
