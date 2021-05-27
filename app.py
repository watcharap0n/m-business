from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import information_table
import uvicorn

app = FastAPI()

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
    information_table.router,
    prefix='/information',
    tags=['marketing info table'],
    responses={418: {'description': "I'm a teapot"}}

)

if __name__ == '__main__':
    uvicorn.run('app:app', debug=True, port=8888)
