from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket
from dependencies.authentication_cookies import cookie_extractor
import os

router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.get('/customers', tags=['Page'])
async def customers(
        request: Request,
        authentication: str = Depends(cookie_extractor)
):
    if authentication:
        return template.TemplateResponse('public/customers.vue', context={'request': request})
    return RedirectResponse(url='/signin')


@router.get('/')
@router.get('/signin')
async def signin(request: Request, authentication: str = Depends(cookie_extractor)):
    if authentication:
        return template.TemplateResponse('public/customers.vue', context={'request': request})
    return template.TemplateResponse('admin/signin.vue', context={'request': request})


@router.get('/intents')
async def intents(request: Request, authentication: str = Depends(cookie_extractor)):
    if authentication:
        return template.TemplateResponse('public/intents.vue', context={'request': request})
    return template.TemplateResponse('admin/signin.vue', context={'request': request})


@router.get('/line/quotation')
async def quotation_line(request: Request):
    return template.TemplateResponse('LINE/quotation.vue', context={'request': request})


@router.get('/facebook/quotation')
async def quotation_facebook(request: Request):
    return template.TemplateResponse('FACEBOOK/quotation.vue', context={'request': request})


@router.post('/customers')
async def customers(
):
    file = os.path.join('static', 'excels/customers.xlsx')
    return FileResponse(file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename='ข้อมูลลูกค้า.xlsx')


"""

test client not in using

"""


@router.get('/test_ws')
async def test_ws(request: Request):
    return template.TemplateResponse('test_ws.vue', context={'request': request})


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    user_dict = {}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        user_dict['user'] = data
        await websocket.send_json(user_dict)
