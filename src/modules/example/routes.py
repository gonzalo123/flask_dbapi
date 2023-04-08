from .actions import foo, bar

routes = [
    dict(route='', action=lambda: True),
    dict(route='foo', action=foo),
    dict(route='bar', action=bar),
]
