from fastapi import APIRouter, Request, HTTPException, Body
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage, MessageEvent
from random import randint
from typing import Optional
from config.db import MongoDB
import json
import os

router = APIRouter()

# line_bot_api_notify = LineBotApi(os.environ['line_bot_api'])
# handler_notify = WebhookHandler(os.environ['handler'])

client = 'mongodb://127.0.0.1:27017'
# client = os.environ.get('MONGODB_URI')
db = MongoDB(database_name='Mango', uri=client)
collection = 'line_bot_notify'


from environ.client_environ import line_bot_api, handler

line_bot_api_notify = LineBotApi(line_bot_api)
handler_notify = WebhookHandler(handler)


def get_profile_notify(user_id):
    profile = line_bot_api_notify.get_profile(user_id)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {'displayName': displayName, 'userId': userId, 'img': img, 'status': status}
    return result


@router.post('/notify')
async def callback_notify(
        request: Request,
        raw_json: Optional[dict] = Body(None)
):
    with open('static/line_log.json', 'w') as log_line:
        json.dump(raw_json, log_line)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = raw_json['events'][0]
        _type = events['type']
        if _type == 'follow':
            userId = events['source']['userId']
            profile = get_profile_notify(userId)
            inserted = {'displayName': profile['displayName'], 'userId': userId, 'img': profile['img'],
                        'status': profile['status']}
            db.insert_one(collection='line_follower', data=inserted)
        elif _type == 'unfollow':
            userId = events['source']['userId']
            db.delete_one('line_follower', query={'userId': userId})
        elif _type == 'postback':
            event_postback_notify(events)
        elif _type == 'message':
            message_type = events['message']['type']
            if message_type == 'text':
                try:
                    handler_notify.handle(str(body, encoding='utf8'), signature)
                except InvalidSignatureError as v:
                    api_error = {'status_code': v.status_code, 'message': v.message}
                    raise HTTPException(status_code=400, detail=api_error)
            else:
                no_event = len(raw_json['events'])
                for i in range(no_event):
                    events = raw_json['events'][i]
                    event_handler_notify(events)
    except IndexError:
        raise HTTPException(status_code=200, detail={'Index': 'null'})
    return raw_json


def event_handler_notify(event):
    replyToken = event['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api_notify.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def event_postback_notify(event):
    pass


@handler_notify.add(MessageEvent, message=TextMessage)
def handler_message_notify(event):
    print(event)
    replyToken = event.reply_token
    message_text = event.message.text
    line_bot_api_notify.reply_message(replyToken, TextSendMessage(text=message_text))
