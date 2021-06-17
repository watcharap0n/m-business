from fastapi import APIRouter, Body, Request
from typing import Optional
from db import MongoDB
from bson import ObjectId
from routers.secure import auth
from object_str import CutId
from routers.items import INTENT_BOT

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'intents'


@router.get('/data')
async def data_intent(request: Request):
    token = request.cookies.get('access_token')
    check = auth.verify_session_cookie(token)
    data = db.find(collection=collection, query={'uid': check['uid']})
    data = list(data)
    for v in data:
        del v['_id']
    return data


@router.post('/add', status_code=201, response_model=INTENT_BOT)
async def add_intent(item: INTENT_BOT):
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
