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

## Firestore Security Rules:
```bash
service cloud.firestore {
  match /databases/{database}/documents {  
    match /test-users/{userId}{    	
        allow read: if request.auth != null;
      
        allow create: if request.auth != null && request.path[4] == request.auth.uid
      					&& 'email' in request.resource.data && request.resource.data.email is string 
  						&& 'notes' in request.resource.data && request.resource.data.notes is map 
          				&& request.resource.data.notes.size() == 0;                     						
                    
        allow update: if isValidUser(userId)  
                        && request.resource.data.email == resource.data.email
                        && request.resource.data.notes is map
                        && request.resource.data.notes.size() > 0;  
    }
  }
}
```