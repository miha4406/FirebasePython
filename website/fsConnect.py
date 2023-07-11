from google.cloud import firestore
from google.oauth2.credentials import Credentials
import datetime


def getDB(dictCred):
    cred = Credentials(dictCred["user"]["stsTokenManager"]['accessToken'])
    db = firestore.Client(project='fbtest-ba697', credentials=cred)

    return db


def registerUser(user): 
    db = firestore.Client(project='fbtest-ba697', credentials=Credentials(user["idToken"]))

    #print(user["email"]); print(user["localId"])
    db.collection("test-users").add( { "email": user["email"], "notes": { } } , user["localId"])
    #db.collection("test-users").add( { "email": dictCred["user"]["email"], "notes": { } } , dictCred["user"]["uid"])

    
def getNotes(dictCred):   #creds as dict 
    db = getDB(dictCred)

    res = db.collection("test-users").document(dictCred["user"]["uid"]).get().to_dict();  

    if len(res) > 0: return res
    else: return None


def getAllNotes(dictCred):
    db = getDB(dictCred)

    res = db.collection("test-users").get()

    lis = []
    for r in res: 
        for el in r.to_dict()["notes"].items():
            lis.append( (el[0], el[1], r.id) );  #print(lis[-1])        
    lis.sort(key=lambda x: datetime.datetime.strptime(x[0], '%H:%M:%S').time() )

    return lis


def addNote(dictCred, text):
    db = getDB(dictCred)

    t = datetime.datetime.now().strftime("%X")    
    db.collection("test-users").document(dictCred["user"]["uid"]).set( { "notes": {t:text} }, merge=True)
    

def delNote(dictCred, key):
    db = getDB(dictCred)
    
    db.collection("test-users").document(dictCred["user"]["uid"]).set( { "notes": {key:firestore.DELETE_FIELD} }, merge=True)
    

def editNote(dictCred, key, text):
    db = getDB(dictCred)
    
    db.collection("test-users").document(dictCred["user"]["uid"]).set( { "notes": {key:text} }, merge=True)
