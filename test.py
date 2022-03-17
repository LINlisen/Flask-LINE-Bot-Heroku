import json

from sqlalchemy import false
with open("Flask-LINE-Bot-Heroku/question.json") as f:
    q = json.load(f)
    print(q[0]['answer'][0]['label'])