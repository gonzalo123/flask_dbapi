from dbutils.dbutils import get_conn, Db, get_cursor

from settings import DATABASES


def get_conn_from_dbname(dbname, named=True, autocommit=True):
    return get_conn(DATABASES.get(dbname), named=named, autocommit=autocommit)


def get_db_from_conn(conn):
    return get_db_from_cursor(get_cursor(conn=conn))


def get_db_from_cursor(cursor):
    return Db(cursor=cursor)
