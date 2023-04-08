import logging
from datetime import datetime
from json import JSONEncoder
from flask import request, jsonify

logger = logging.getLogger(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def find_route(name, routes):
    for route in routes:
        if name == route['route']:
            return route
    return False


def call_action(name, data, routes):
    route = find_route(name, routes)
    if route:
        if data:
            return 200, route['action'](**data)
        else:
            return 200, route['action']()
    else:
        logger.error('Route not found')
        return 400, 'route not found'


def get_response(blueprint, name, routes, action):
    start = datetime.now()
    data = request.json if request.is_json else None
    status_code, body = action(name, data, routes)

    response = jsonify(body)
    response.status_code = status_code

    diff = (datetime.now() - start)
    logger.info(f"Done {blueprint}/{name} in {diff.total_seconds()} seconds.")

    return response
