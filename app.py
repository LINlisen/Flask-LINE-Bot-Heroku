import os
from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackAction,ButtonsTemplate,PostbackEvent
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('app/dtd-linebot-firebase-adminsdk-s4c8a-182e518a38.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'User').document(u'QEfFnDfWPM9qv1tCVA9q')


with open("/app/question.json") as f:
    q = json.load(f)




app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:z1x2c3v441@IP:3306/db_name"


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
    user_id = event.source.user_id
    print("user_id =", user_id)
    docs = doc_ref.get()
    local_dict=docs.to_dict()
    if(user_id not in local_dict.keys()):
        new_user={user_id:0}
        local_dict.update(new_user)
        doc_ref.set(local_dict)
    get_message = event.message.text
    if get_message == '開始問答':
        
        docs = doc_ref.get()
        local_dict=docs.to_dict()
        templete_button=Starting_Qusetion(local_dict[user_id])
        try:
            line_bot_api.reply_message(event.reply_token,templete_button) 
        except LineBotApiError as e:
            print(e)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))    
        
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    print("user_id =", user_id)
    get_postback = event.postback.data
    print(get_postback)
    docs = doc_ref.get()
    local_dict=docs.to_dict()
    if(get_postback == '答對'):
        try:
            local_dict[user_id]=local_dict[user_id]+1
            doc_ref.set(local_dict)
            docs = doc_ref.get()
            local_dict=docs.to_dict()
            if(local_dict[user_id] == 3):
                try:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage('獲得獎勵！'))
                except LineBotApiError as e:
                    print(e)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage('發生錯誤！'))
            else:
                next_templete_button=Starting_Qusetion(local_dict[user_id])
                print(next_templete_button)
                line_bot_api.reply_message(event.reply_token,next_templete_button) 
        except LineBotApiError as e:
            print(e)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    else:
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(get_postback+'! 請重新點擊開始答題')) 
        except LineBotApiError as e:
            print(e)
            line_bot_api.reply_message(event.reply_token,TextSendMessage('發生錯誤！'))
    
