from fastapi import APIRouter, HTTPException
from models.transaction import Transaction
from bson import ObjectId
from config.db import MongoDB
from config.object_str import CutId
import datetime
import os

router = APIRouter()
client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'imports'


@router.post('/data/quotation', response_model=Transaction)
async def data_quotation(item: Transaction):
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
