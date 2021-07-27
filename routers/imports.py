from fastapi import APIRouter, Path, Body
from typing import Optional
import datetime
from db import MongoDB
from object_str import CutId
from bson import ObjectId
from models.transaction import Transaction
from modules.SortingDateTime import SortingDate
from modules.Export_excel import ExportExcel
from starlette.responses import FileResponse
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


@router.post('/import', status_code=201, response_model=Transaction)
async def import_post(item: Transaction):
    key = CutId(_id=ObjectId()).dict()['id']
    item = item.dict()
    _d = datetime.datetime.now()
    item["date"] = _d.strftime("%d/%m/%y")
    item["time"] = _d.strftime("%H:%M:%S")
    item["id"] = key
    db.insert_one(collection=collection, data=item)
    del item['_id']
    return item


@router.put('/import/{id}')
async def import_put(
        item: Transaction,
        id: Optional[str] = Path(None)
):
    payload = item.dict()
    _d = datetime.datetime.now()
    query = {'id': id}
    values = {'$set': payload}
    db.update_one(collection=collection, values=values, query=query)
    return {'message': 'success'}


@router.delete('/import/{id}', status_code=204)
async def import_delete(id: Optional[str] = Path(None)):
    db.delete_one(collection=collection, query={'id': id})
    return {'message': 'success'}


@router.get('/m/sorting/')
async def import_sorting(start: Optional[str] = None, end: Optional[str] = None):
    sorting_date = SortingDate(collection=collection, after_start_date=start, before_end_date=end)
    data = sorting_date.createDataFrame()
    data = data.to_dict('records')
    return data


@router.post('/datafile/import/excel')
async def customers_excel(id: Optional[list] = Body([])):
    excel = ExportExcel(db, collection, id).excel()
    excel.save()
    file = os.path.join('static', 'excels/customers.xlsx')
    return FileResponse(file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename='imports.xlsx')
