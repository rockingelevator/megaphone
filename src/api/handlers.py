import asyncio
import sqlalchemy as sa
from aiohttp import web
from utils.utils import json_response, is_iterable
from src.handlers import check_if_user_in_team
from src import models


def to_json(handler):
    async def wrapped(request, **kwargs):
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        n_list = await handler(request, limit=limit, offset=offset)
        items = [dict(row) for row in n_list] if is_iterable(n_list) else []
        result = {
            'meta': {
                'offset': offset,
                'limit': limit
            },
            'items': items
        }
        return json_response(result, **kwargs)
    return wrapped


@to_json
@check_if_user_in_team
@asyncio.coroutine
def notifications(request, team=None, limit=20, offset=0):
    with(yield from request.app['db']) as conn:
        n = models.notifications.alias()
        n_query = sa.select([n])\
            .where(n.c.team == team['id'])\
            .order_by(sa.desc(n.c.creation_date))\
            .limit(limit)\
            .offset(offset)
        return (yield from conn.execute(n_query))





