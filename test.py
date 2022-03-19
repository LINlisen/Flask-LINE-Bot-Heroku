import json
from time import sleep
with open("data.json") as g:
    s = json.load(g)
print(s)
new_user={"amy":2}
s.update(new_user)
with open("data.json",'w',encoding='utf-8') as h:
    json.dump(s, h,ensure_ascii=False)
with open("data.json") as g:
    s = json.load(g)
name = "amy"
print(s[name])