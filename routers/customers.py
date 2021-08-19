from fastapi import APIRouter, Path, Body
from fastapi.responses import FileResponse
from typing import Optional
import datetime
from config.db import MongoDB
from config.object_str import CutId
from bson import ObjectId
from models.transaction import Transaction
from modules.pandasModules import DataColumnFilter
import os

router = APIRouter()

client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'customers'


@router.get('/customer')
async def customers_get():
    data = db.find(collection=collection, query={})
    data = list(data)
    for v in data:
        del v['_id']
    products = set([v['product'] for v in data if v['product']])
    channels = set([v['channel'] for v in data if v['channel']])
    tags = set([v['tag'][0] for v in data if v['tag']])
    return {
        'transaction': data[::-1],
        'products': products,
        'channels': channels,
        'tags': tags
    }


@router.post('/customer', status_code=201, response_model=Transaction)
async def customers_post(item: Transaction):
    key = CutId(_id=ObjectId()).dict()['id']
    item = item.dict()
    _d = datetime.datetime.now()
    item["date"] = _d.strftime("%d/%m/%y")
    item["time"] = _d.strftime("%H:%M:%S")
    item["id"] = key
    db.insert_one(collection=collection, data=item)
    del item['_id']
    return item


@router.put('/customer/{id}')
async def customers_put(
        item: Transaction,
        id: Optional[str] = Path(None)
):
    payload = item.dict()
    _d = datetime.datetime.now()
    query = {'id': id}
    values = {'$set': payload}
    db.update_one(collection=collection, values=values, query=query)
    return {'message': 'success'}


@router.delete('/customer/{id}', status_code=204)
async def customer_delete(id: Optional[str] = Path(None)):
    db.delete_one(collection=collection, query={'id': id})
    return {'message': 'success'}


@router.post('/customer/delete/multiple', status_code=204)
async def customers_delete(items: Optional[list] = Body(...)):
    for i in items:
        db.delete_one(collection=collection, query={'id': i['id']})
    return {'message': 'success'}


@router.post('/move/customer')
async def move_customer(items: Optional[list] = Body(None)):
    for d in items:
        db.delete_one(collection='imports', query={'id': d['id']})
    for v in items:
        _d = datetime.datetime.now()
        key = CutId(_id=ObjectId()).dict()['id']
        v['id'] = key
        v['date_insert'] = _d.strftime("%d/%m/%y")
        v['time_insert'] = _d.strftime("%H:%M:%S")
    db.insert_many(collection=collection, data=items)
    return {'message': 'success'}


@router.post('/c/sorting/')
async def customer_sorting(item: Optional[dict] = Body(None)):
    product = item['product']
    channel = item['channel']
    date = item['date']
    tag = item['tag']
    
    if not date:
        sorting = DataColumnFilter(collection=collection, database=db, product=product, channel=channel, tag=tag)
        dfs = sorting.filter()
        data = sorting.sorting_table(dfs=dfs)
        data = data.to_dict('records')
        return data
    sorting = DataColumnFilter(collection=collection, after_start_date=date[0], before_end_date=date[1], database=db,
                               product=product, channel=channel, tag=tag)
    dfs = sorting.filter()
    data = sorting.sorting_table(dfs=dfs)
    data = data.to_dict('records')
    return data


@router.post('/datafile/customer/excel')
async def customers_excel(id: Optional[list] = Body(None)):
    excel = DataColumnFilter(id=id, database=db, collection=collection)
    excel.export_excel().save()
    file = os.path.join('static', 'excels/customers.xlsx')
    return FileResponse(file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename='customers.xlsx')
