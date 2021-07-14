from fastapi import APIRouter, HTTPException, Body
from routers.models import FROM_MANGO, UserItem
from bson import ObjectId
from typing import List
from db import MongoDB
from object_str import CutId
import datetime
import os

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'api_receive_mango'


@router.post('/cors_mango', response_model=FROM_MANGO)
async def cors_mango(item: FROM_MANGO):
    try:
        key = CutId(_id=ObjectId()).dict()['id']
        item = item.dict()
        _d = datetime.datetime.now()
        item['name'] = item.pop('firstname')
        item["date"] = _d.strftime("%d/%m/%y")
        item["time"] = _d.strftime("%H:%M:%S")
        item["id"] = key
        db.insert_one(collection=collection, data=item)
        del item['_id']
        return item
    except:
        raise HTTPException(status_code=400, detail='API Something wrong!')


@router.post('/test_api', response_model=UserItem)
async def test_api(item: UserItem):
    return item

