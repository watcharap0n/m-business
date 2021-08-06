from fastapi import APIRouter, Body
from typing import Optional
from config.db import MongoDB
from bson import ObjectId
from config.object_str import CutId
from models.intent_bot import Intent
import os

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'intents'


@router.post('/data')
async def data_intent(access_token: Optional[dict] = Body(None)):
    access_token = access_token['access_token']
    data = db.find(collection=collection, query={'access_token': access_token})
    data = list(data)
    for v in data:
        del v['_id']
    return data


@router.post('/add', status_code=201, response_model=Intent)
async def add_intent(item: Intent):
    key = CutId(_id=ObjectId()).dict()['id']
    item = item.dict()
    item['id'] = key
    db.insert_one(collection=collection, data=item)
    return item


@router.get('/query/{id}')
async def query_intent(id: Optional[str] = None):
    data = db.find_one(collection=collection, query={'id': id})
    data = dict(data)
    del data['_id']
    return {'message': data}


@router.post('/update_intent')
async def update_intent(
        data: Optional[dict] = Body(None),
):
    id = data.get('id')
    query = {'id': id}
    values = {'$set': data}
    db.update_one(collection=collection, query=query, values=values)
    return {'message': 'success'}


@router.delete('/delete_intent/{id}')
async def delete_intent(
        id: Optional[str] = None
):
    db.delete_one(collection=collection, query={'id': id})
    return {'message': 'success'}
