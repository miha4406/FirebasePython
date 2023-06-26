from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from website import firestoreDB, storage



views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@views.route("/<userid>", methods=["GET", "POST"])
def userPage(userid):
    
    avaURL = ""

    if request.method == "GET":
        if userid != session["userid"]: pageNotFound(404) 
        else:
            try:
                avaURL = storage.readAva(session["userid"])
            except:
                print("Can't read an avatar!")    


    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1: flash("Message too short!", category="error")
        else: 
            try:
                firestoreDB.addNote(session["userid"], note)
                flash("Message added.", category="ok")
            except:     
                flash("Can't add message to Firestore!", category="error") 
            finally:
                session["userdata"] = firestoreDB.getNotes(session["userid"])  #not safe?

    return render_template("home.html", avaURL=avaURL)


@views.route("/forum", methods=["GET","POST"])
def forum():

    noteList = firestoreDB.getAllNotes()  #can be None?

    if request.method == "GET":
        return render_template("forum.html", noteList=noteList)
    
    if request.method == "POST":
        
        sKey = request.form.get("searchBar")

        res = filter(lambda el: sKey.lower() in el[1].lower(), noteList)

        return render_template("forum.html", noteList=res, sKey=sKey)


@views.route("/notes/delete/<string:key>")
def noteDelete(key):
    #triggers on GET by link
    try:
        firestoreDB.delNote(session["userid"], key) 
        flash("Message deleted.", category="ok")
    except:
        flash("Can't delete!", category="error")  
    finally:
        session["userdata"] = firestoreDB.getNotes(session["userid"])

    return redirect(url_for("views.userPage", userid=session["userid"]))    


@views.route("/notes/edit/<string:key>", methods=["GET", "POST"])
def noteEdit(key):

    if request.method == "GET":
        return render_template("note.html", key=key)
    
    if request.method == "POST":

        note = request.form.get("note1")

        if len(note) < 1: flash("Message too short!", category="error")
        else:
            try:
                firestoreDB.editNote(session["userid"], key, note) 
                flash("Message edited.", category="ok")
            except:
                flash("Can't edit!", category="error")  
            finally:
                session["userdata"] = firestoreDB.getNotes(session["userid"])

    return redirect(url_for("views.userPage", userid=session["userid"]))


@views.route("/avatar", methods=["GET", "POST"])
def uploadAva():

    fName = request.form.get("ava");  print(fName)
    
    try:
        storage.uploadAva(session["userid"], fName)
        flash("New avatar uploaded.", category="ok")
    except:
        flash("Can't upload!", category="error")  


    return redirect(url_for("views.userPage", userid=session["userid"]))


@views.app_errorhandler(404)
def pageNotFound(e):
    return render_template("404.html"), 404