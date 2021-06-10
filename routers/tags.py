from fastapi import APIRouter, Path, Query
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


@router.get('/tag')
async def find_tag(tag: Optional[str] = None):
    if tag:
        lst = [tag]
        key = CutId(_id=ObjectId()).dict()['id']
        data = {'tags': lst, 'id': key}
        db.insert_one(collection='tags_customer', data=data)
        return 'success'
    data = db.find(collection=collection, query={})
    data = list(data)
    for v in data:
        del v['_id']
    return data[::-1]


@router.put('/tag/{item}', description='add tag to database')
async def add_tag(
        item: Optional[str] = Path(..., title='append tag', description='append tag keep to the MongoDB'),
        q: Optional[str] = Query(..., alias="id-query", description='ID Tag Query MongoDB')):
    data = db.find_one(collection=collection, query={'id': q})
    data['tags'].append(item)
    return {'item': item, 'q': q}
