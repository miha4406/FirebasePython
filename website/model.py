from google.cloud import firestore
import google.oauth2.credentials

import flask
from flask import app
import google_auth_oauthlib.flow


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = "https://www.googleapis.com/auth/datastore" # https://www.googleapis.com/auth/cloud-platform


app = flask.Flask(__name__)
app.secret_key = 'secretKey123'  # https://flask.palletsprojects.com/quickstart/#sessions


@app.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')
  
    cred = google.oauth2.credentials.Credentials(**flask.session['credentials'])

    #do something
    return 


@app.route('/authorize')
def authorize():
  # flow instance to manage the OAuth 2.0 Authorization Grant Flow steps
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file( CLIENT_SECRETS_FILE, scopes=SCOPES)

  # authorized redirect URI, configured in the API Console
  flow.redirect_uri = flask.url_for('auCallback', _external=True)

  authorization_url, state = flow.authorization_url( access_type='offline', include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)


@app.route('/auCallback')
def auCallback():
  
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('auCallback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)
  
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.redirect(flask.url_for('test_api_request'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'id_token': credentials.id_token}



if __name__ == '__main__':  app.run('localhost', 8080, debug=True)





def getCreds():
   
    #flask.session['state'] = state
    #state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    #flow.redirect_uri = flask.url_for('auCallback', _external=True)
    authorization_url, state = flow.authorization_url( access_type='offline', include_granted_scopes='true')

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
  
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    



#old
def registerUser(user):  

    cred = google.oauth2.credentials.Credentials(**flask.session['credentials'])        
    
    db = firestore.Client(project='fbtest-ba697', credentials=cred); #print(str(user["localId"]))

    db.collection("users").add( { "email": user["email"], "messages": { } } , user["localId"])




    '''doc = db.collection('users').document(str(user["localId"]))
    doc.set({"email": user["email"]})
    doc.collection("posts").set( {"timestamp": firestore.SERVER_TIMESTAMP, "text" : "User registered."}, merge=True )'''

