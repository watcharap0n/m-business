from fastapi import FastAPI, Request, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dependent.authentication_cookies import cookie_extractor
from fastapi.responses import RedirectResponse
from routers import customers, imports, tags, wh_client, secure, api_cors, intents
import time
import uvicorn
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(docs_url='/docs_kane')
app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://mango-client.herokuapp.com",
    "https://mangoconsultant.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    cookie = request.cookies.get('color')
    if cookie:
        page = template.TemplateResponse('admin/signin.vue', context={'request': request})
        return page
    elif not cookie:
        page = template.TemplateResponse('admin/signin.vue', context={'request': request})
        page.set_cookie(key='color', value='#000000')
        return page


@app.get('/intents', tags=['Page'])
async def intents(request: Request):
    return template.TemplateResponse('public/intents.vue', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app:app', debug=True, port=8888)
