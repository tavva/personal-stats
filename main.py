import os
import base64
import flask
import hashlib
import secrets
import requests

from urllib.parse import urlencode
from replit import db

from auth import login_required

app = flask.Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
)

@app.route('/')
@login_required
def home():
    return "Home"

@app.route('/login')
def login():
    if flask.g.user_id:
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('login.html')

@app.before_request
def load_user():
    flask.g.user_id = flask.request.headers.get('X-Replit-User-Id')

# Read access token from DB
# Attempt to connect
# If failed, get refresh token from DB
# (If no refresh token, fail with error message saying we need one, show: https://pdwhomeautomation.blogspot.com/2016/01/fitbit-api-access-using-oauth20-and.html)
# Use refresh token to get access token
# Save access token to DB
# Attempt to connect
# If fail, error with message


#access_token = db.get('access_token')

#if not access_token:
#    refresh_access_token()

@app.route('/redirect')
def handle_redirect_from_fitbit():
    code = flask.request.args.get('code')
    if not code:
        flask.abort(404)

    db[f"authorisation_code:{flask.g.user_id}"] = code

    params = {
        "client_id": os.environ["FITBIT_CLIENT_ID"],
        "code": code,
        "code_verifier": db[f"code_verifier:{flask.g.user_id}"],
        "grant_type": "authorization_code",
    }
    
    url = "https://api.fitbit.com/oauth2/token"
    response = requests.post(url, data=params)

    data = response.json()

    db[f"access_token:{flask.g.user_id}"] = data['access_token']
    db[f"refresh_token:{flask.g.user_id}"] = data['refresh_token']
    
    return "Authorised."

@app.route('/authorise')
def request_authorisation():
    code_verifier = secrets.token_urlsafe(43)
    db[f"code_verifier:{flask.g.user_id}"] = code_verifier

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8")[:-1]
    
    params = {
        "client_id": os.environ["FITBIT_CLIENT_ID"],
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": "weight",
    }
    
    authorization_url = "https://www.fitbit.com/oauth2/authorize?" + urlencode(params)
    return flask.redirect(authorization_url)
    
    
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=3000,
    )