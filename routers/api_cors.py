from fastapi import APIRouter, HTTPException, Body
from routers.models import Transaction, UserItem
from bson import ObjectId
from db import MongoDB
from object_str import CutId
import datetime
from typing import Optional
from linebot.models import TextSendMessage
from routers.wh_notify import line_bot_api_notify
import os

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'imports'


@router.post('/cors_mango', response_model=Transaction)
async def cors_mango(item: Transaction):
    key = CutId(_id=ObjectId()).dict()['id']
    item = item.dict()
    _d = datetime.datetime.now()
    item["date"] = _d.strftime("%d/%m/%y")
    item["time"] = _d.strftime("%H:%M:%S")
    item["id"] = key
    db.insert_one(collection=collection, data=item)
    name = item['name']
    product = item['product']
    tel = item['tel']
    line_bot_api_notify.broadcast(
        TextSendMessage(text=f'แจ้งเตือน! คุณ {name} ขอใบเสนอราคาตัว {product} ติดต่อเบอร์ {tel}'))
    del item['_id']
    return item


@router.post('/get_demo', status_code=201)
async def get_demo(item: Optional[dict] = Body(None)):
    print('Here ITEM IS : ')
    print(item)
    return item

@router.post('/contact', status_code=201)
async def contact(item: Optional[dict] = Body(None)):
    print('Here ITEM IS : ')
    print(item)
    return item
