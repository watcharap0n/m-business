from pydantic import BaseModel, Field
from typing import Optional


class Customers_id(BaseModel):
    id: Optional[list] = Field(None, example='id MongoDb (Array)')