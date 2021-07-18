from pydantic import BaseModel
from typing import Optional


# access token and secret token of webhook chatbot
class TokenLINE(BaseModel):
    ACCESS_TOKEN: Optional[str] = None
    SECRET_LINE: Optional[str] = None
