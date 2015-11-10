import ujson
from aiohttp import web


def is_iterable(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def json_response(data, **kwargs):
    kwargs.setdefault('content_type', 'application/json')
    return web.Response(text=ujson.dumps(data), **kwargs)


if __name__ == "__main__":
    data = [{"first_name": "Django", "last_name": "Freeman"}]
    json_response(data)