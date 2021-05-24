from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import secure, information_table
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    secure.router,
    prefix='/secure',
    tags=['secure'],
    responses={418: {'description': "I'm a teapot"}},
)

app.include_router(
    information_table.router,
    prefix='/information',
    tags=['marketing info table'],
    responses={418: {'description': "I'm a teapot"}}

)


@app.get('/', tags=['page public'])
def root_login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@app.get('/mk/info_table', tags=['page marketing'])
def root_info_table(request: Request):
    return templates.TemplateResponse('mk/information_table.html', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app:app', debug=True, port=8888)
