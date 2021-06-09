from fastapi import APIRouter, Path, HTTPException
from typing import Optional
import datetime
from db import MongoDB
from object_str import CutId
from bson import ObjectId
from routers.items import Transaction
import os

client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'imports'

router = APIRouter()


@router.get('/import')
async def import_get():
    data = db.find(collection=collection, query={})
    data = list(data)
    for v in data:
        del v['_id']
    return data[::-1]


@router.post('/import', status_code=201)
async def import_post(item: Transaction):
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


@router.put('/import/{id}')
async def import_put(
        item: Transaction,
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


@router.delete('/import/{id}')
async def import_delete(id: Optional[str] = Path(None)):
    db.delete_one(collection=collection, query={'id': id})
    return 'success'