from pydantic import BaseModel, Field
from typing import Optional, List


class Customers_id(BaseModel):
    id: Optional[List] = Field(None, example='id MongoDb (Array)')