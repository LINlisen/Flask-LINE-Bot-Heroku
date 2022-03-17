import json
from time import sleep
with open("data.json") as g:
    s = json.load(g)

dict={"score":4}
with open("data.json",'w',encoding='utf-8') as h:
    json.dump(dict, h,ensure_ascii=False)
sleep(1)   
print(s['score'])