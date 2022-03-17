import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackAction,ButtonsTemplate

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if get_message == '開始問答':
        try:
            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://example.com/image.jpg',
                    title='問題一',
                    text='請問數位系總共有幾個攤位',
                    actions=[
                        PostbackAction(
                            label='5',
                            display_text='5',
                            data='答錯'
                        ),
                        PostbackAction(
                            label='11',
                            display_text='11',
                            data='答錯'
                        ),
                        PostbackAction(
                            label='13',
                            display_text='13',
                            data='答對'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,buttons_template_message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

