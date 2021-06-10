from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routers import customers, imports, tags, wh_client
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://mango-client.herokuapp.com",
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

@app.get('/customers', tags=['Page'])
async def customers(request: Request):
    return template.TemplateResponse('customers.vue', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app:app', debug=True, port=8888)
