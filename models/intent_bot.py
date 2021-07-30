from pydantic import BaseModel
from typing import Optional, List


# machine learning of the chat bot in the provide customers
class Intent(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    question: Optional[List] = None
    answer: Optional[List] = None
    uid: Optional[str] = None
    access_token: Optional[str] = None