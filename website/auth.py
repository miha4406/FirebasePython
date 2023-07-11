import pyrebase
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from requests.exceptions import HTTPError
from website import fsConnect #,firestoreDB
import json


with open("keys/fbConfig.json") as jf:
    firebaseConfig = json.load(jf)
firebase = pyrebase.initialize_app(firebaseConfig)
fbau = firebase.auth()
fbstor = firebase.storage()


def addUser(req):    
    user = fbau.create_user_with_email_and_password(req["email"], req["pass1"])  #print(user)
           
    #firestoreDB.registerUser(user)  #need creds!
    fsConnect.registerUser(user)
    

def logoutUser():
    #fbau.signOut()
    fbau.current_user = None    
    


##FLASK CODE
auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":
        req = dict(request.form) #print(req["email"])
        
        if len(req["email"]) < 4:
            flash("Email < 4!", category="error")
        elif len(req["fName"]) < 2:
            flash("Name < 2!", category="error")
        elif len(req["pass1"]) < 6:
            flash("Password < 6!", category="error")
        elif req["pass1"] != req["pass2"]:
            flash("Pass1 != pass2!", category="error")
        else:             
            try:
                addUser(req)
                flash("Account created!", category="ok")
            except HTTPError as er:            
                flash(er.strerror, category="error")

    return render_template("signup.html")


@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        strCred = request.get_json().get("cred", "")  #print(cred.get("cred", ""))
        dictCred = json.loads(strCred) #to dict
        session["dictCred"] = dictCred

        if dictCred:
            flash("Welcome!", category="ok")

            session["userid"] = dictCred["user"]["uid"]; #print(session["userid"])            
        else: print("Cred is None!")
        try:            
            session["userdata"] = fsConnect.getNotes(dictCred)
            return redirect(url_for("views.userPage", userid=session["userid"]))
        except HTTPError as er:            
            flash(er.strerror, category="error")  

    return render_template("login.html") 

def login0():
        
    if request.method == "POST":
        req = dict(request.form)
        
        try:
            login = fbau.sign_in_with_email_and_password(req["email"], req["pass"]) #cant pass it to db
            flash("Welcome!", category="ok");  #print(fbau.get_account_info(login["idToken"])); 
                                       
            session["userid"] = login["localId"]
            session["userdata"] = firestoreDB.getNotes(login["localId"])            
            return redirect(url_for("views.userPage", userid=login["localId"]))
            #fbau.get_account_info(login["idToken"])['users'][0]['email'],     
            #render_template("home.html", userdata=firestoreDB.getMessages(login["localId"]))                                              
        except HTTPError as er:            
            flash(er.strerror, category="error")  

    return render_template("login.html") 


@auth.route("/logout")
def logout():

    logoutUser(); session.clear()

    return redirect(url_for("views.home" ))
    #return render_template("logout.html")


@auth.route('/firebase-config')
def get_firebase_config():
    global firebaseConfig

    return jsonify(firebaseConfig) 