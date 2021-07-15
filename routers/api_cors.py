from fastapi import APIRouter, HTTPException, Body
from routers.models import Transaction, UserItem
from bson import ObjectId
from db import MongoDB
from object_str import CutId
import datetime
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
    del item['_id']
    return item


@router.post('/test_api', response_model=UserItem)
async def test_api(item: UserItem):
    return item
