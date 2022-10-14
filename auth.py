import flask

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not flask.g.get('user_id'):
            return flask.redirect(
                flask.url_for('login', next=flask.request.url),
            )
        return f(*args, **kwargs)
        
    return decorated_function