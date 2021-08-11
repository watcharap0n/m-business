from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import customers, imports, tags, wh_client, secure, api_cors, intents, quotation, wh_notify, pages
import time
import uvicorn
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(docs_url='/docs/doc', redoc_url='/docs/redoc')
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://www.mangoconsultant.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    pages.router,
    tags=['Page'],
    responses={418: {'description': "I'm a teapot"}}
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8005))
    uvicorn.run('app:app', debug=True, port=port)
