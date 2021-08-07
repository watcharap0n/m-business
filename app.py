from fastapi import FastAPI, Request, Depends
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dependencies.authentication_cookies import cookie_extractor
from fastapi.responses import RedirectResponse
from starlette.websockets import WebSocket
from routers import customers, imports, tags, wh_client, secure, api_cors, intents, quotation, wh_notify
import time
import uvicorn
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(docs_url='/docs/doc', redoc_url='/docs/redoc')
app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

origins = [
    'https://572666a1f922.ngrok.io',
    "http://127.0.0.1:5000",
    "http://www.mangoconsultant.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    customers.router,
    prefix='/api',
    tags=['Table Customers'],
    responses={418: {'description': "I'm a teapot"}}

)

app.include_router(
    imports.router,
    prefix='/api',
    tags=['Table Import'],
    responses={418: {'description': "I'm a teapot"}}
)

app.include_router(
    tags.router,
    prefix='/api',
    tags=['Tags'],
    responses={418: {'description': "i'm a teapot"}}
)

app.include_router(
    wh_client.router,
    prefix='/callback',
    tags=['Callback'],
    responses={418: {'description': "i'm a teapot"}}
)

app.include_router(
    secure.router,
    prefix='/secure',
    tags=['Secure'],
    responses={418: {'description': "I'm a teapot"}}
)

app.include_router(
    api_cors.router,
    prefix='/cors',
    tags=['CORS'],
    responses={418: {'description': "I'm a teapot"}}
)

app.include_router(
    intents.router,
    prefix='/intent',
    tags=['Intents'],
    responses={418: {'description': "I'm a teapot"}}
)

app.include_router(
    quotation.router,
    prefix='/quotation',
    tags=['Quotation'],
    responses={418: {'description': "I'm a teapot"}}
)

app.include_router(
    wh_notify.router,
    prefix='/mango',
    tags=['notify'],
    responses={418: {'description': "I'm a teapot"}}
)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(round(process_time, 5))
    return response


@app.get('/customers', tags=['Page'])
async def customers(
        request: Request,
        authentication: str = Depends(cookie_extractor)
):
    if authentication:
        return template.TemplateResponse('public/customers.vue', context={'request': request})
    return RedirectResponse(url='/signin')


@app.get('/')
@app.get('/signin', tags=['Page'])
async def signin(request: Request, authentication: str = Depends(cookie_extractor)):
    if authentication:
        return template.TemplateResponse('public/customers.vue', context={'request': request})
    return template.TemplateResponse('admin/signin.vue', context={'request': request})


@app.get('/intents', tags=['Page'])
async def intents(request: Request, authentication: str = Depends(cookie_extractor)):
    if authentication:
        return template.TemplateResponse('public/intents.vue', context={'request': request})
    return template.TemplateResponse('admin/signin.vue', context={'request': request})


@app.get('/line/quotation', tags=['Page'])
async def quotation_line(request: Request):
    return template.TemplateResponse('LINE/quotation.vue', context={'request': request})


@app.get('/facebook/quotation', tags=['Page'])
async def quotation_facebook(request: Request):
    return template.TemplateResponse('FACEBOOK/quotation.vue', context={'request': request})


@app.get('/test_ws')
async def test_ws(request: Request):
    return template.TemplateResponse('test_ws.vue', context={'request': request})


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    user_dict = {}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        user_dict['user'] = data
        await websocket.send_json(user_dict)


@app.post('/customers', tags=['Page'])
async def customers(
):
    file = os.path.join('static', 'excels/customers.xlsx')
    return FileResponse(file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename='ข้อมูลลูกค้า.xlsx')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8005))
    uvicorn.run('app:app', debug=True, port=port)
