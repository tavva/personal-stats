import flask

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(flask.request.headers)
        if flask.g.user_id is None:
            return flask.redirect(
                flask.url_for('login', next=flask.request.url),
            )
        return f(*args, **kwargs)
        
    return decorated_function