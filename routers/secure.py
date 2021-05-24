from fastapi import APIRouter, File, UploadFile, Form, Depends, Response, Request, HTTPException
from fastapi_login import LoginManager
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from db import MongoDB
import os
from typing import Optional
from firebase_admin import auth
import json
from auth.firebase import Config_firebase
# from auth.token_firebase import set_authentication, set_firebase

with open('auth/firebase.json', 'r') as json_file:
    load_json = json.load(json_file)
    client_firebase = load_json['firebase']
    client_credential = load_json['credential']

router = APIRouter()
SECRET = 'watcharaponweeraborirak'
manager = LoginManager(SECRET, tokenUrl='/secure/login', use_cookie=True)
config = Config_firebase(path_db=client_firebase, path_auth=client_credential)
pb = config.authentication()
# var_mongodb = os.environ['MONGODB_URI']
# db = MongoDB(database_name='Poker', uri=var_mongodb)
db = MongoDB(database_name='linebot_mango', uri='mongodb://127.0.0.1:27017')


@manager.user_loader
async def load_user(email: Optional[str] = None, password: Optional[str] = None):
    """[manager login]

    Args:
        email (Optional[str], optional): [description]. Defaults to None.
        password (Optional[str], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    user = pb.sign_in_with_email_and_password(email, password)
    return user


def response_cookies(user, response):
    """[response_cookies]

    Args:
        user ([type]): [description]
        response ([type]): [description]

    Returns:
        [type]: [description]
    """
    auth_cookie = auth.create_session_cookie(
        id_token=user['idToken'], expires_in=timedelta(hours=1))
    check_verify = auth.get_user_by_email(email=user['email'])
    verify_email = check_verify.email_verified
    manager.set_cookie(response, str(auth_cookie))
    return verify_email


@router.post('/login')
async def login(
        response: Response,
        data: OAuth2PasswordRequestForm = Depends(),
        remember: list = Form(...)
):
    """[login]

    Args:
        response (Response): [description]
        data (OAuth2PasswordRequestForm, optional): [description]. Defaults to Depends().
        remember (list, optional): [description]. Defaults to Form(...).

    Returns:
        [type]: [description]
    """
    email = data.username
    password = data.password
    try:
        if remember == ['checked']:
            user = await load_user(email, password)
            response.set_cookie(key='email_login', value=email)
            response.set_cookie(key='password_login', value=password)
            verify_email = response_cookies(user, response)
            if verify_email:
                return {'message': user, 'status': True}
            pb.send_email_verification(user['idToken'])
            return {'message': 'please check your email to verify your account', 'fg': True}
        user = await load_user(email, password)
        verify_email = response_cookies(user, response)
        if verify_email:
            return {'message': user, 'status': True}
        pb.send_email_verification(user['idToken'])
        return {'message': 'please check your email to verify your account', 'fg': True}
    except:
        return {'message': 'Email or Password Invalid', 'status': False}


@router.post('/register')
async def register(
        request: Request,
        file: UploadFile = File(...),
        email: str = Form(...),
        password: str = Form(...),
        username: str = Form(...),
):
    """[register]

    Args:
        request (Request): [description]
        file (UploadFile, optional): [description]. Defaults to File(...).
        email (str, optional): [description]. Defaults to Form(...).
        password (str, optional): [description]. Defaults to Form(...).
        username (str, optional): [description]. Defaults to Form(...).

    Returns:
        [type]: [description]
    """
    host = request.url.hostname
    scheme = request.url.scheme
    port = request.url.port
    domain_path = f'{scheme}://{host}:{port}'
    uploads_dir = os.path.join('static', 'uploads')
    file_input = os.path.join(uploads_dir, file.filename)
    https_dir = os.path.join(domain_path, file_input)
    user = auth.create_user(
        email=email,
        password=password,
        display_name=username,
        photo_url=https_dir
    )
    data = {
        'email': email,
        'password': password,
        'username': username,
        'photo_url': https_dir,
    }
    db.insert_one(collection='register', data=data)
    with open(file_input, 'wb+') as uploads_file:
        uploads_file.write(file.file.read())
        uploads_file.close()
    return {'user': user}


@router.get('/cookie_login')
async def cookies_login(request: Request):
    email = request.cookies.get('email_login')
    password = request.cookies.get('password_login')
    return {'email': email, 'password': password}


@router.post('/forgot_password')
async def forgot_password(email: str = Form(...)):
    pb.send_password_reset_email(email)
    return {'email': 'please check your email'}


@router.get('/cookie_clear')
async def cookie_clear(response: Response):
    response.delete_cookie('email_login')
    response.delete_cookie('password_login')
    return {'status': 'success'}


@router.get('/logout')
async def clean_session(response: Response, request: Request):
    token = request.cookies.get('access-token')
    if not token:
        return RedirectResponse(url='/root_login')
    try:
        decoded_claims = auth.verify_session_cookie(token, check_revoked=True)
        auth.revoke_refresh_tokens(decoded_claims['sub'])
        response.set_cookie('access-token', value='logout', expires=0)
        return RedirectResponse(url='/root_login')
    except auth.RevokedSessionCookieError:
        return RedirectResponse(url='/root_login')
    except auth.InvalidSessionCookieError:
        return RedirectResponse(url='/root_login')
