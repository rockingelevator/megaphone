import asyncio
import json
import sqlalchemy as sa
import datetime
from aiohttp import web, MsgType
from utils.utils import json_response, is_iterable
from aiohttp_session import get_session
from src.handlers import check_if_user_in_team
from src import models
import src.api.schemas as schemas


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


@check_if_user_in_team
@asyncio.coroutine
def notifications(request, team=None, limit=20, offset=0):
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))
    with(yield from request.app['db']) as conn:
        nf = models.notifications.alias()
        us = models.users.alias()
        items = []
        nf_count = 0;
        trans = yield from conn.begin()

        try:
            nf_count = yield from conn.scalar(sa.select([sa.func.count(nf.c.id)])
                                          .where(nf.c.team == team['id']))

            nf_query = sa.select([nf])\
                .where(nf.c.team == team["id"])\
                .order_by(sa.desc(nf.c.creation_date))\
                .limit(limit)\
                .offset(offset)
            nfs = yield from conn.execute(nf_query)
            for n in nfs:
                item = dict(n)
                author_query = sa.select([us]).where(us.c.id == item["author"])
                author = yield from conn.execute(author_query)
                item["author"] = yield from author.fetchone()
                items.append(item)
        except Exception:
            yield from trans.rollback()
        else:
            yield from trans.commit()

        schema = schemas.NotificationSchema(many=True)
        result = {
            'meta': {
                'offset': offset,
                'limit': limit,
                'total': nf_count
            },
            'items': schema.dump(items).data
        }

        return json_response(result)


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
            author=session['user_id'],
            type=type,
            message=message,
            creation_date=datetime.datetime.now()
        )
        if(yield from conn.execute(ins_query)):
            return web.HTTPCreated()
        else:
            return web.HTTPBadRequest(reason='Error while saving')


@asyncio.coroutine
def create_notification(request, type, message, team_id):
    if not type:
        raise ValueError("type arg is required")
    if not message:
        raise ValueError("message arg is required")
    if not team_id:
        raise ValueError("team_id arg is required")

    session = yield from get_session(request)

    with(yield from request.app['db']) as conn:
        ins_query = models.notifications.insert().values(
            team=team_id,
            author=session['user_id'],
            type=type,
            message=message,
            creation_date=datetime.datetime.now()
        )
        if(yield from conn.execute(ins_query)):
            return
        else:
            raise AssertionError('can not save notification')

@asyncio.coroutine
def users(request, **kwargs):
    with(yield from request.app['db']) as conn:
        query = sa.select([models.users])
        ret = yield from conn.execute(query)
        schema = schemas.UserSchema(many=True)
        result = schema.dump(list(ret))
        #items = [schema.dump(row).data for row in ret] if is_iterable(ret) else []
        return json_response(result.data)


@asyncio.coroutine
def teams(request):
    with(yield from request.app['db']) as conn:
        trans = yield from conn.begin()
        result = []
        try:
            query = sa.select([models.teams])
            teams = yield from conn.execute(query)
            for row in teams:
                item = dict(row)
                owner = yield from conn.execute(sa.select([models.users])\
                                                        .where(models.users.c.id == item['owner']))
                item['owner'] = yield from owner.fetchone()
                result.append(item)
        except Exception:
            yield from trans.rollback()
        else:
            yield from trans.commit()
        schema = schemas.TeamSchema(many=True)
        return json_response(schema.dump(result).data)


@check_if_user_in_team
@asyncio.coroutine
def notifications_websocket_handler(request, team=None):

    ws = web.WebSocketResponse()
    yield from ws.prepare(request)

    while not ws.closed:
        msg = yield from ws.receive()

        if msg.tp == MsgType.text:
            if msg.data == 'close':
                yield from ws.close()
            else:
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError:
                    print('To create a notification pass data')
                else:
                    try:
                        c = yield from create_notification(request, data['type'], data['message'], team['id'])
                    except AssertionError as e:
                        print(str(e))
                    except Exception as e:
                        print(str(e))
                    else:
                        print('Created!')


        elif msg.tp == MsgType.close:
            print('websocket connection closed')
        elif msg.tp == MsgType.error:
            print('ws connection closed with exception %s' % ws.exception())

    return ws
