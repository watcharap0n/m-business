from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers import secure
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

app.include_router(
    secure.router,
    prefix='/secure',
    tags=['secure'],
    responses={418: {'description': "I'm a teapot"}},
)


@app.route('/')
def root_login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app:app', debug=True, port=8888)
