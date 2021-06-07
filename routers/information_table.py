from fastapi import APIRouter, Path, HTTPException
from typing import Optional
from pydantic import BaseModel
import datetime
from db import MongoDB
from object_str import CutId
from bson import ObjectId
import os

router = APIRouter()

client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='dashboard', uri=client)
collection = 'mango'



class Item(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    tel: Optional[str] = None
    product: Optional[str] = None
    company: Optional[str] = None
    channel: Optional[str] = None
    tag: Optional[list] = None


@router.get('/table')
async def info_table_get():
    data = db.find(collection=collection, query={})
    data = list(data)
    for v in data:
        del v['_id']
    return data[::-1]  # เอาข้อมูลล่าสุด


@router.post('/table', status_code=201)
async def info_table_post(item: Item):
    print(item.dict())
    try:
        key = CutId(_id=ObjectId()).dict()['id']
        item = item.dict()
        _d = datetime.datetime.now()
        item["date"] = _d.strftime("%d/%m/%y")
        item["time"] = _d.strftime("%H:%M:%S")
        item["id"] = key
        db.insert_one(collection=collection, data=item)
        del item['_id']
        return item
    except:
        raise HTTPException(status_code=400, detail='API Something wrong!')


@router.put('/table/{id}')
async def info_table_put(
        item: Item,
        id: Optional[str] = Path(None)
):
    payload = item.dict()
    _d = datetime.datetime.now()
    query = {'id': id}
    payload['date'] = _d.strftime("%d/%m/%y")
    payload['time'] = _d.strftime("%H:%M:%S")
    values = {'$set': payload}
    db.update_one(collection=collection, values=values, query=query)
    return 'success'


@router.delete('/table/{id}')
async def info_table_delete(id: Optional[str] = Path(None)):
    db.delete_one(collection=collection, query={'id': id})
    return 'success'
