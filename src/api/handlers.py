import ujson
import asyncio
import sqlalchemy as sa
from utils.json_response import json_response
from src.handlers import check_if_user_in_team
from src import models


@check_if_user_in_team
@asyncio.coroutine
def notifications(request, team):
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))
    with(yield from request.app['db']) as conn:
        n = models.notifications.alias()
        n_query = sa.select([n])\
            .where(n.c.team == team['id'])\
            .order_by(sa.desc(n.c.creation_date))\
            .limit(limit)\
            .offset(offset)
        n_list = yield from conn.execute(n_query)
        result = {
            'meta': {
                'offset': offset,
                'limit': limit
            },
            'items': [dict(row) for row in n_list]
        }
        return json_response(result)



