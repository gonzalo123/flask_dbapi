## Flask api skeleton to handle PostgreSQL operations

That`s a boilerplate for an api server using Flask. The idea is one api server to work as backend server to handle 
all database operations. The api server will handle only POST requests and the input parameters will be on the body 
of the payload as JSON. I know that it isn't a pure REST server but that's what I need.

To organize better the api we`ll set a group of modules using Flask's blueprints. The entry point of the application 
will be app.py file

```python
import logging

from flask import Flask
from flask_compress import Compress

from lib.logger import setup_logging
from lib.utils import CustomJSONEncoder
from modules.example import blueprint as example
from settings import LOG_LEVEL, ELK_APP, ELK_INDEX, ELK_PROCESS, LOG_PATH

logging.basicConfig(level=LOG_LEVEL)

setup_logging(app=ELK_APP,
              index=ELK_INDEX,
              process=ELK_PROCESS,
              log_path=LOG_PATH)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
compress = Compress()
compress.init_app(app)

app.register_blueprint(example)
```
All application configuration is in settings.py file. I borrow this pattern from Django applications. All my 
configuration is in this file and the particularities of the environment are loaded from dotenv files in settings.py  

```python
import os
from logging import INFO
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

APP_ID = 'dbapi'
APP_PATH = 'dbapi'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

load_dotenv(dotenv_path=Path(BASE_DIR).resolve().joinpath('env', ENVIRONMENT, '.env'))

PROCESS_ID = os.getenv('PROCESS_ID', APP_ID)
LOG_LEVEL = os.getenv('LOG_LEVEL', INFO)
ELK_APP = f'{APP_ID}.{PROCESS_ID}'
ELK_INDEX = f'{APP_ID}_{ENVIRONMENT}'
ELK_PROCESS = APP_ID
LOG_PATH = f'./logs/{APP_ID}.log'

BEARER = os.getenv('BEARER')

# Database configuration
DEFAULT = 'default'

DATABASES = {
    DEFAULT: f"dbname='{os.getenv('DEFAULT_DB_NAME')}' user='{os.getenv('DEFAULT_DB_USER')}' host='{os.getenv('DEFAULT_DB_HOST')}' password='{os.getenv('DEFAULT_DB_PASS')}' port='{os.getenv('DEFAULT_DB_PORT')}'"
}
```

In this example we're using one blueprint called example. I register blueprints manually. The blueprint has a set or 
routes. Those routes are within routes.py file:

```python
from .actions import foo, bar

routes = [
    dict(route='', action=lambda: True),
    dict(route='foo', action=foo),
    dict(route='bar', action=bar),
]
```

Here we map url path to actions. For example foo action is like that


```python
from datetime import datetime

from lib.decorators import use_schema
from .schemas import FooSchema


@use_schema(FooSchema)
def foo(name, email=False):
    now = datetime.now()
    return dict(name=name, email=email, time=now)
```

To validate user input we're using schemas (using marshmallow library). In this example our validation schema is:

```python
from marshmallow import fields, Schema


class FooSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=False)
```

We're hiding Flask infrastructure path in module's __init__.py file

```python
import os

from flask import Blueprint

from lib.auth import authorize_bearer
from lib.utils import call_action, get_response
from settings import BEARER
from .routes import routes

NAME = os.path.basename(os.path.dirname(__file__))
blueprint = Blueprint(NAME, __name__, url_prefix=f'/{NAME}')


@authorize_bearer(bearer=BEARER)
@blueprint.post('/')
@blueprint.post('/<path:name>')
def action(name=''):
    return get_response(NAME, name, routes, call_action)
```

Another route with a database connection is the following one:

```python
from dbutils import transactional

from lib.db import get_db_from_conn, get_conn_from_dbname
from lib.decorators import use_schema, inject_conn
from settings import DEFAULT
from .schemas import FooSchema
from .sql import SQL_USERS


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
```

We can obtain our database connection from different ways. For example, we can use a function decorator to inject 
the connection (in this case the connection named DEFAULT) in the function signatura. We also can create the 
connection using a constructor. This connection is a raw psycopg2 connection. I also like to use a library to help 
me to work with psycopg2: a library (https://github.com/gonzalo123/dbutils) created by me time ago.

And that's all. I normally deploy it in production using a nginx as a reverse proxy and n replicas of my api. Logs 
are also ready to send to ELK using a filebeat.

```yaml
version: '3.6'

x-logging: &logging
  logging:
    options:
      max-size: 10m


services:
  api:
    image: dbapi:production
    <<: *logging
    deploy:
      replicas: 10
      restart_policy:
        condition: any
    volumes:
      - logs_volume:/src/logs
    environment:
      - ENVIRONMENT=production
    command: /bin/bash ./start.sh

  nginx:
    image: nginx-dbapi:${VERSION}
    deploy:
      restart_policy:
        condition: any
    environment:
      ENVIRON: ${VERSION}
    ports:
      - ${EXPOSED_PORT}:8000
    depends_on:
      - api

volumes:
  logs_volume:
```


