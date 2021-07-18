from pydantic import BaseModel
from typing import Optional


# machine learning of the chat bot in the provide customers
class Intent(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    question: Optional[list] = None
    answer: Optional[list] = None
    uid: Optional[str] = None
    access_token: Optional[str] = None