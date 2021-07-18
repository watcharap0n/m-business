from fastapi import APIRouter, HTTPException, Body
from routers.models import Transaction, UserItem
from bson import ObjectId
from db import MongoDB
from object_str import CutId
import datetime
from typing import Optional
from features_line.flex_message import flex_notify_channel
from routers.wh_notify import line_bot_api_notify
import os
import pytz

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'imports'


@router.post('/cors_mango', response_model=Transaction)
async def cors_mango(item: Transaction):
    tz = pytz.timezone('Asia/Bangkok')
    key = CutId(_id=ObjectId()).dict()['id']
    item = item.dict()
    _d = datetime.datetime.now(tz)
    item["date"] = _d.strftime("%d/%m/%y")
    item["time"] = _d.strftime("%H:%M:%S")
    item["id"] = key
    db.insert_one(collection=collection, data=item)
    name = item['name']
    product = item['product']
    tel = item['tel']
    channel = item['channel']
    date = item['date']
    time = item['time']
    email = item['email']
    message = item['message']
    company = item['company']
    print(name, product, tel, channel, date, time, email, message, company)
    line_bot_api_notify.broadcast(
        flex_notify_channel(channel=channel, date_time=f'{date} {time}', company=company, name=name, tel=tel,
                            email=email, product=product, message=message))
    del item['_id']
    return item


def key_model_transaction(item: dict, channel: str):
    item['other'] = None
    item['userId'] = None
    item['email_private'] = None
    item['profile'] = None
    item['picture'] = None
    item['channel'] = channel
    item['username'] = None
    item['uid'] = None
    item['tag'] = []
    return item


@router.post('/get_demo', status_code=201)
async def get_demo(item: Optional[dict] = Body(None)):
    tz = pytz.timezone('Asia/Bangkok')
    key = CutId(_id=ObjectId()).dict()['id']
    _d = datetime.datetime.now(tz)
    item['name'] = item.pop('fname')
    item["date"] = _d.strftime("%d/%m/%y")
    item["time"] = _d.strftime("%H:%M:%S")
    item["id"] = key
    item = key_model_transaction(item, 'GetDemo')
    db.insert_one(collection=collection, data=item)
    name = item['name']
    product = item['product']
    tel = item['tel']
    channel = item['channel']
    date = item['date']
    time = item['time']
    email = item['email']
    message = item['message']
    company = item['company']
    del item['_id']
    if company == 'google':
        return item
    else:
        print(name, product, tel, channel, date, time, email, message, company)
        line_bot_api_notify.broadcast(
            flex_notify_channel(channel=channel, date_time=f'{date} {time}', company=company, name=name, tel=tel,
                                email=email, product=product, message=message))
    return item


@router.post('/contact', status_code=201)
async def contact(item: Optional[dict] = Body(None)):
    tz = pytz.timezone('Asia/Bangkok')
    key = CutId(_id=ObjectId()).dict()['id']
    _d = datetime.datetime.now(tz)
    item['email'] = item.pop('contact_email')
    item['name'] = item.pop('contact_name')
    item['company'] = item.pop('contact_name_company')
    item['product'] = item.pop('contact_subject')
    item['tel'] = item.pop('contact_tel')
    item['message'] = item.pop('contact_message')
    item["date"] = _d.strftime("%d/%m/%y")
    item["time"] = _d.strftime("%H:%M:%S")
    item["id"] = key
    del item['contact_email_div']
    item = key_model_transaction(item, 'Contact')
    db.insert_one(collection=collection, data=item)
    name = item['name']
    product = item['product']
    tel = item['tel']
    channel = item['channel']
    date = item['date']
    time = item['time']
    email = item['email']
    message = item['message']
    company = item['company']
    del item['_id']
    if company == 'google':
        return item
    else:
        print(name, product, tel, channel, date, time, email, message, company)
        line_bot_api_notify.broadcast(
            flex_notify_channel(channel=channel, date_time=f'{date} {time}', company=company, name=name, tel=tel,
                                email=email, product=product, message=message))
    return item
