## To use Flask SQL: 
```bash
pip install flask-sqlalchemy
```
## To redirect to Home page:
```bash
return redirect(url_for("views.home"))
```
## To get idToken:
```bash
login = loginwith...
login["idToken"]
```

## If you have troubles installing a Pyrebase:
1) Try different versions of pyrebase, available on pypi.org (pyrebase4 worked for me)
2) Check for pyrebase requirements and install them all
3) If you already have different version of some dependencies, reinstall it using ```pip install --force reinstall "module==version"``` syntax
4) If console message warns you about something else, install/update it too
5) If it warns about a missing key, add this key to firebaseConfig