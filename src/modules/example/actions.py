from datetime import datetime

from dbutils import transactional

from lib.db import get_db_from_conn, get_conn_from_dbname
from lib.decorators import use_schema, inject_conn
from settings import DEFAULT
from .schemas import FooSchema
from .sql import SQL_USERS


@use_schema(FooSchema)
def foo(name, email=False):
    now = datetime.now()
    return dict(name=name, email=email, time=now)


@use_schema(FooSchema)
@inject_conn(DEFAULT, named=True, autocommit=False)
def bar(conn, name, email=False):
    # Create new transaction from connection injected with a decorator
    with transactional(conn) as db:
        db.upsert('users', dict(email=email), dict(name=name))

    # Example of how to obtain new connection from database name.
    conn2 = get_conn_from_dbname(DEFAULT)
    db2 = get_db_from_conn(conn2)

    return db2.fetch_all(SQL_USERS, dict(name=name))
