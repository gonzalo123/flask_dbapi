import logging
from functools import wraps

from flask import request

from lib.db import get_conn_from_dbname

logger = logging.getLogger(__name__)


def use_schema(schema):
    def authorize(f):
        @wraps(f)
        def decorated_function(*args, **kws):
            data = request.json
            errors = schema().validate(data)
            if errors:
                logger.error(errors)
                return 400, errors

            return f(*args, **kws)

        return decorated_function

    return authorize


def inject_conn(dbname, named=True, autocommit=False):
    def get_db(f):
        @wraps(f)
        def decorated_function(*args, **kws):
            kws['conn'] = get_conn_from_dbname(dbname, named=named, autocommit=autocommit)
            return f(*args, **kws)

        return decorated_function

    return get_db
