from fastapi import APIRouter, Request, HTTPException, Body, Path
from typing import Optional
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage, MessageEvent
import json
from routers.items import TokenLINE
from random import randint
import os
from db import MongoDB


# client = os.environ.get('MONGODB_URI')
client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='dashboard', uri=client)
collection = 'line_bot'
line_bot_api = LineBotApi("")
handler = WebhookHandler("")

router = APIRouter()


def get_profile(user_id):
    profile = line_bot_api.get_profile(user_id)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {'displayName': displayName, 'userId': userId, 'img': img, 'status': status}
    return result


@router.post('/save')
async def save():
    pass


@router.post('/webhook/{token}')
async def webhook(
        request: Request,
        token: Optional[str] = Path(...),
        raw_json: Optional[dict] = Body(None)
):
    data = {'user': 'kane', 'token': f'/callback/webhook/{token}'}
    db.insert_one(collection=collection, data=data)
    with open('static/line_log.json', 'w') as log_line:
        json.dump(raw_json, log_line)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = raw_json['events'][0]
        _type = events['type']
        if _type == 'follow':
            userId = events['source']['userId']
            profile = get_profile(userId)
            inserted = {'displayName': profile['displayName'], 'userId': userId, 'img': profile['img'],
                        'status': profile['status']}
            db.insert_one(collection='line_follower', data=inserted)
        elif _type == 'unfollow':
            userId = events['source']['userId']
            db.delete_one('line_follower', query={'userId': userId})
        elif _type == 'postback':
            event_postback(events)
        elif _type == 'message':
            message_type = events['message']['type']
            if message_type == 'text':
                try:
                    userId = events['source']['userId']
                    message = events['message']['text']
                    profile = get_profile(userId)
                    push_message = {'user_id': userId, 'message': message, 'display_name': profile['displayName'],
                                    'img': profile['img'],
                                    'status': profile['status']}
                    db.insert_one(collection='message_user', data=push_message)
                    handler.handle(str(body, encoding='utf8'), signature)
                except InvalidSignatureError as v:
                    api_error = {'status_code': v.status_code, 'message': v.message}
                    raise HTTPException(status_code=400, detail=api_error)
            else:
                no_event = len(raw_json['events'])
                for i in range(no_event):
                    events = raw_json['events'][i]
                    event_handler(events)
    except IndexError:
        raise HTTPException(status_code=200, detail={'Index': 'null'})
    return raw_json


def event_handler(events):
    replyToken = events['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def event_postback(events):
    pass


@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    replyToken = event.reply_token
    message_text = event.message.text
    print(message_text, replyToken)
