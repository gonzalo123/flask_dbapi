from functools import wraps

from flask import request, abort


def authorize_bearer(bearer):
    def authorize(f):
        @wraps(f)
        def decorated_function(*args, **kws):
            if 'Authorization' not in request.headers:
                abort(401)

            data = request.headers['Authorization']
            if str.replace(str(data), 'Bearer ', '') != bearer:
                abort(401)

            return f(*args, **kws)

        return decorated_function

    return authorize
