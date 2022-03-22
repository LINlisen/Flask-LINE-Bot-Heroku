import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('dtd-linebot-firebase-adminsdk-s4c8a-182e518a38.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'User').document(u'QEfFnDfWPM9qv1tCVA9q')

docs = doc_ref.get()

print(type(docs))
c=docs.to_dict()
if 'Lin' not in c.keys():
    new_data={"Lin":0}
    c.update(new_data)
    doc_ref.set(c)
print(type(c.values()))
print(c.keys())
print(f'{(docs.to_dict()).values()} ')
