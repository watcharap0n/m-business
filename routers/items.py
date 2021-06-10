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


class TokenLINE(BaseModel):
    ACCESS_TOKEN: Optional[str] = None
    SECRET_LINE: Optional[str] = None
    WEBHOOK: Optional[str] = None
