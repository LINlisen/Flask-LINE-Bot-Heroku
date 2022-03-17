import os
from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackAction,ButtonsTemplate,PostbackEvent

import json


with open("/app/question.json") as f:
    q = json.load(f)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

count = 0

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
    

def Starting_Qusetion(q_num):
    buttons_template_message = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://example.com/image.jpg',
                        title='問題'+str(q_num+1),
                        text=q[q_num]['text'],
                        actions=[
                            PostbackAction(
                                label=q[q_num]['answer'][0]['label'],
                                display_text=q[q_num]['answer'][0]['label'],
                                data=q[q_num]['answer'][0]['data']
                            ),
                            PostbackAction(
                                label=q[q_num]['answer'][1]['label'],
                                display_text=q[q_num]['answer'][1]['label'],
                                data=q[q_num]['answer'][1]['data']
                            ),
                            PostbackAction(
                                label=q[q_num]['answer'][2]['label'],
                                display_text=q[q_num]['answer'][2]['label'],
                                data=q[q_num]['answer'][2]['data']
                            ),
                        ]
                    )
                )  
    return(buttons_template_message)            



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if get_message == '開始問答':
        templete_button=Starting_Qusetion(count)
        try:
            line_bot_api.reply_message(event.reply_token,templete_button) 
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))    
        
@handler.add(PostbackEvent)
def handle_postback(event):
    get_postback = event.postback.data
    print(get_postback)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(get_postback))
    if(get_postback == '答對'):
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='恭喜答對！'))
            count+=1
            templete_button=Starting_Qusetion(count)
            line_bot_api.reply_message(event.reply_token,templete_button) 
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    else:
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='答錯！'))
            templete_button=Starting_Qusetion(count)
            line_bot_api.reply_message(event.reply_token,templete_button) 
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    if(count==2):
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='獲得獎勵！'))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))