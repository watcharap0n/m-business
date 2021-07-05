from fastapi import APIRouter, HTTPException, Body
from routers.items import FROM_MANGO
from bson import ObjectId
from db import MongoDB
from object_str import CutId
import datetime
import os

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'quotation'


@router.post('/data/quotation', response_model=FROM_MANGO)
async def data_quotation(item: FROM_MANGO):
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
