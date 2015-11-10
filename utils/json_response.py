import ujson
from aiohttp import web


def json_response(data, **kwargs):
    kwargs.setdefault('content_type', 'application/json')
    return web.Response(text=ujson.dumps(data), **kwargs)


if __name__ == "__main__":
    data = [{"first_name": "Django", "last_name": "Freeman"}]
    json_response(data)