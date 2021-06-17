from fastapi import APIRouter, Request, HTTPException, Body, Path
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage, MessageEvent
from model_text_classifire import intent_model
from routers.items import TokenLINE
from random import randint
from bson import ObjectId
from object_str import CutId
from typing import Optional
from db import MongoDB
from numpy import random
import uuid
import json
import os

client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'line_bot'

router = APIRouter()


@router.post('/save')
async def save(item: TokenLINE):
    key = CutId(_id=ObjectId()).dict()['id']
    path_wh = uuid.uuid4().hex
    result = item.dict()
    result['id'] = key
    result['token'] = path_wh
    result['webhook'] = f'https://m-bussiness-bot.herokuapp.com/callback/{path_wh}'
    db.insert_one(collection=collection, data=result)
    del result['_id']
    return result


def get_profile(user_id, q):
    line_bot_api = q['ACCESS_TOKEN']
    line_bot_api = LineBotApi(line_bot_api)
    profile = line_bot_api.get_profile(user_id)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {'displayName': displayName, 'userId': userId, 'img': img, 'status': status}
    return result


@router.post('/{token}')
async def webhook(
        request: Request,
        token: Optional[str] = Path(...),
        raw_json: Optional[dict] = Body(None)
):
    # client_token = 'c96bf514c5264bf7a72acd8290f1cff0'
    q = db.find_one(collection=collection, query={'token': token})
    q = dict(q)
    handler = q['SECRET_LINE']
    handler = WebhookHandler(handler)
    with open('static/line_log.json', 'w') as log_line:
        json.dump(raw_json, log_line)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = raw_json['events'][0]
        _type = events['type']
        if _type == 'follow':
            userId = events['source']['userId']
            profile = get_profile(userId, q)
            inserted = {'displayName': profile['displayName'], 'userId': userId, 'img': profile['img'],
                        'status': profile['status']}
            db.insert_one(collection='line_follower', data=inserted)
        elif _type == 'unfollow':
            userId = events['source']['userId']
            db.delete_one('line_follower', query={'userId': userId})
        elif _type == 'postback':
            event_postback(events, q)
        elif _type == 'message':
            message_type = events['message']['type']
            if message_type == 'text':
                try:
                    userId = events['source']['userId']
                    message = events['message']['text']
                    profile = get_profile(userId, q)
                    push_message = {'user_id': userId, 'message': message, 'display_name': profile['displayName'],
                                    'img': profile['img'],
                                    'status': profile['status']}
                    db.insert_one(collection='message_user', data=push_message)
                    handler.handle(str(body, encoding='utf8'), signature)
                    handler_message(events, q)
                except InvalidSignatureError as v:
                    api_error = {'status_code': v.status_code, 'message': v.message}
                    raise HTTPException(status_code=400, detail=api_error)
            else:
                no_event = len(raw_json['events'])
                for i in range(no_event):
                    events = raw_json['events'][i]
                    event_handler(events, q)
    except IndexError:
        raise HTTPException(status_code=200, detail={'Index': 'null'})
    return raw_json


def event_handler(events, q):
    line_bot_api = q['ACCESS_TOKEN']
    line_bot_api = LineBotApi(line_bot_api)
    replyToken = events['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def event_postback(events, q):
    pass


def handler_message(events, q):
    line_bot_api = q['ACCESS_TOKEN']
    line_bot_api = LineBotApi(line_bot_api)
    text = events['message']['text']
    replyToken = events['replyToken']
    user_id = events['source']['userId']
    data = intent_model(text, q['ACCESS_TOKEN'])
    if data.get('require'):
        line_bot_api.reply_message(replyToken, TextSendMessage(text=data.get('require')))
    label = data['predict']
    choice_answers = data['answers']
    confident = data['confident'][0] * 100
    user = get_profile(user_id, q)
    displayName = user['displayName']
    if confident > 69:
        choice = random.choice(choice_answers[int(label)])
        line_bot_api.reply_message(replyToken, TextSendMessage(text=choice))
    else:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='ฉันไม่เข้าใจ'))

