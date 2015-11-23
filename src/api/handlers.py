import asyncio
import sqlalchemy as sa
import datetime
from aiohttp import web
from utils.utils import json_response, is_iterable
from aiohttp_session import get_session
from src.handlers import check_if_user_in_team
from src import models
from .schemas import UserSchema, TeamSchema


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
        stmt = sa.select([models.users.c.id])\
            .where(models.users.c.id == n.c.author_id)\
            .correlate(n)
        enclosing_smt = sa.select([models.users, n])\
            .select_from(models.users.join(n))\
            .where(models.users.c.id == stmt)
        return (yield from conn.execute(enclosing_smt))



@check_if_user_in_team
@asyncio.coroutine
def add_notification(request, team=None):
    data = yield from request.post()
    type = data.get('type', '')
    message = data.get('message', '')
    if not type or not message:
        return web.HTTPBadRequest(reason='Type and message are required')
    session = yield from get_session(request)
    with(yield from request.app['db']) as conn:
        ins_query = models.notifications.insert().values(
            team=team['id'],
            author_id=session['user_id'],
            type=type,
            message=message,
            creation_date=datetime.datetime.now()
        )
        if(yield from conn.execute(ins_query)):
            return web.HTTPCreated()
        else:
            return web.HTTPBadRequest(reason='Error while saving')


@asyncio.coroutine
def users(request, **kwargs):
    with(yield from request.app['db']) as conn:
        query = sa.select([models.users])
        ret = yield from conn.execute(query)
        schema = UserSchema(many=True)
        result = schema.dump(list(ret))
        #items = [schema.dump(row).data for row in ret] if is_iterable(ret) else []
        return json_response(result.data)


@asyncio.coroutine
def teams(request):
    with(yield from request.app['db']) as conn:
        query = sa.select([models.teams])
        ret = yield from conn.execute(query)
        result = []
        for row in ret:
            item = dict(row)
            owner = yield from conn.execute(sa.select([models.users])\
                                                    .where(models.users.c.id == item['owner']))
            item['owner'] = yield from owner.fetchone()
            result.append(item)
        schema = TeamSchema(many=True)
        result = schema.dump(result)
        return json_response(result.data)

