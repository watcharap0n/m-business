from pydantic import BaseModel, Field
from typing import Optional, List

CUSTOMER = 'CUSTOMER'


# data transaction of table customers
class Transaction(BaseModel):
    id: Optional[str] = Field(None, example='id MongoDb (string)')
    person_id: Optional[str] = Field(None, example='person_id (string)')
    tax_id: Optional[str] = Field(None, example='tax_id (string)')
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
    tag: Optional[List] = None
    date: Optional[str] = None
    time: Optional[str] = None

