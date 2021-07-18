from linebot.models import (FlexSendMessage)
from typing import Optional


def flex_notify_channel(channel: Optional[str] = '', date_time: Optional[str] = '', company: Optional[str] = '',
                        name: Optional[str] = '',
                        tel: Optional[str] = '', email: Optional[str] = '', product: Optional[str] = '',
                        message: Optional[str] = ''):
    flex_msg = FlexSendMessage(
        alt_text='Notify! customer contact',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": channel,
                                "size": "sm",
                                "color": "#AAAAAA",
                                "flex": 1,
                                "align": "start",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": date_time,
                                "size": "sm",
                                "color": "#666666",
                                "flex": 3,
                                "align": "end",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "กรุณาติดต่อกลับ",
                        "weight": "bold",
                        "size": "lg",
                        "margin": "md",
                        "contents": []
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "บริษัท",
                                        "size": "sm",
                                        "color": "#AAAAAA",
                                        "flex": 1,
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": company,
                                        "size": "sm",
                                        "color": "#666666",
                                        "flex": 5,
                                        "wrap": True,
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "ติดต่อ",
                                        "size": "sm",
                                        "color": "#AAAAAA",
                                        "flex": 1,
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": name,
                                        "size": "sm",
                                        "color": "#666666",
                                        "flex": 5,
                                        "wrap": True,
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "โทร.",
                                        "size": "sm",
                                        "color": "#AAAAAA",
                                        "flex": 1,
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": tel,
                                        "size": "sm",
                                        "color": "#666666",
                                        "flex": 5,
                                        "wrap": True,
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Email",
                                        "size": "sm",
                                        "color": "#AAAAAA",
                                        "flex": 1,
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": email,
                                        "size": "sm",
                                        "color": "#666666",
                                        "flex": 5,
                                        "wrap": True,
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "สนใจ",
                                        "size": "sm",
                                        "color": "#AAAAAA",
                                        "flex": 1,
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": product,
                                        "size": "sm",
                                        "color": "#666666",
                                        "flex": 5,
                                        "wrap": True,
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "รายละเอียดเพิ่มเติม",
                                "size": "sm",
                                "color": "#AAAAAA",
                                "margin": "md",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": message,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                ]
            }
        }
    )
    return flex_msg
