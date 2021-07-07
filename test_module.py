from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from db import MongoDB
from object_str import CutId
import datetime
import os
import json

router = APIRouter()
# client = os.environ.get('MONGODB_URI')
client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'customers'


with open('data.json', 'r') as json_file:
    read_data = json.load(json_file)
    data = read_data['RestCustomer']

dst = {}
key = list(data)
data = [data[i] for i in data]
to_id = CutId(_id=ObjectId()).dict()['id']
for i in data:
    i['id'] = to_id
    i['email_private'] = i.pop('emailliff')
    i['uid'] = ''
    del i['authorized']
    del i['tax']
    del i['position']

# print(data[1])


db.insert_many(collection, data)





