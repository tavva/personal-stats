import flask

app = flask.Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
)

# Read access token from DB
# Attempt to connect
# If failed, get refresh token from DB
# (If no refresh token, fail with error message saying we need one, show: https://pdwhomeautomation.blogspot.com/2016/01/fitbit-api-access-using-oauth20-and.html)
# Use refresh token to get access token
# Save access token to DB
# Attempt to connect
# If fail, error with message

import auth
auth.request_authorisation()

def refresh_access_token():
    refresh_token = db['refresh_token']

    


#access_token = db.get('access_token')

#if not access_token:
#    refresh_access_token()

@app.route('/redirect')
def redirect():
    code = flask.request.args.get('code')
    if not code:
        flask.abort(404)
    return code

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=3000,
    )