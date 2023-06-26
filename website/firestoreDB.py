import firebase_admin
from firebase_admin import firestore, credentials
import datetime


cred = credentials.Certificate("keys/serAccKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  #project='fbtest-ba697', credentials=cred


def registerUser(user):        
       
    db.collection("test-users").add( { "email": user["email"], "notes": { } } , user["localId"])

    
def getNotes(userId):
    
    res = db.collection("test-users").document(userId).get().to_dict();  #print(res)
    #res = db.collection("users").document(str(userId)).collection("messages").get()

    if len(res) > 0: return res
    else: return None


def getAllNotes():

    res = db.collection("test-users").get()

    lis = []
    for r in res: 
        for el in r.to_dict()["notes"].items():
            lis.append( (el[0], el[1], r.id) );  #print(lis[-1])
        #lis.append( {r.id : r.to_dict()["notes"]} ); #print(lis[-1])
    lis.sort(key=lambda x: datetime.datetime.strptime(x[0], '%H:%M:%S').time() )

    return lis
        


def addNote(userId, text):
    t = datetime.datetime.now().strftime("%X")
    #db.collection("users").document(userId).collection("messages").add( { "date3" : text })
    #db.collection("users").document(userId).update({ "notes": firestore.ArrayUnion([{t:text}]) })
    #db.collection("users").document(userId).update({"messages": {str(3) : text}})
    db.collection("test-users").document(userId).set( { "notes": {t:text} }, merge=True)
    

def delNote(userId, key):
    
    db.collection("test-users").document(userId).set( { "notes": {key:firestore.DELETE_FIELD} }, merge=True)
    

def editNote(userId, key, text):
    
    db.collection("test-users").document(userId).set( { "notes": {key:text} }, merge=True)
