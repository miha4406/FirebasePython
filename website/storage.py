import os


def uploadAva(userId, fName):
    from website import auth

    auth.fbstor.child("test-users").child(userId+".png").put(os.getcwd()+"/website/templates/"+fName) 


def readAva(userId):
    from website import auth

    url = auth.fbstor.child("test-users").child(userId+".png").get_url(token=None)  #no need in test mode
    
    return url