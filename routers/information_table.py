from fastapi import APIRouter
import json

router = APIRouter()

with open('auth/chatbot-mango-export-2.json', 'r') as json_file:
    load_json = dict(json.load(json_file))
    data = [load_json[x] for x in load_json.keys()]


@router.get('/table')
def info_table_get():
    return data


@router.post('/table')
def info_table_post():
    pass


@router.put('/table')
def info_table_put():
    pass


@router.delete('/table')
def info_table_delete():
    pass
