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
