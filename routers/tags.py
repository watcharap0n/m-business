from fastapi import APIRouter, Path, Query, Body
from db import MongoDB
from object_str import CutId
from typing import Optional
from bson import ObjectId
import os

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'tags_customer'


@router.get('/tag', status_code=201)
async def find_tag(tag: Optional[str] = None):
    if tag:
        key = CutId(_id=ObjectId()).dict()['id']
        data = {'text': tag, 'id': key}
        db.insert_one(collection='tags_customer', data=data)
        return {'message': 'success'}
    data = db.find(collection=collection, query={})
    data = list(data)
    for v in data:
        del v['_id']
    return data[::-1]


@router.put('/tag/{item}', description='add tag to database')
async def add_tag(
        item: Optional[str] = Path(..., title='append tag', description='append tag keep to the MongoDB'),
        id: Optional[str] = Query(..., alias="id-query", description='ID Tag Query MongoDB')):
    query = {'id': id}
    values = {'$set': {'text': item}}
    db.update_one(collection=collection, query=query, values=values)
    return {'item': item, 'q': id}


@router.delete('/tag', description='delete tag to database')
async def delete_tag(
        id: Optional[str] = Query(..., alias='id-query')
):
    db.delete_one(collection=collection, query={'id': id})
    return {'message': 'success'}


@router.post('/tag')
async def post_tag(item: Optional[dict] = None):
    id = item['id']
    value = [x['text'] for x in item['tag']]
    for i in id:
        db.update_one(collection='customers', query={'id': i['id']}, values={'$set': {'tag': value}})
    return item
