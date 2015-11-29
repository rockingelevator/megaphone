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


# @check_if_user_in_team
# @asyncio.coroutine
# def add_notification(request, team=None):
#     data = yield from request.post()
#     type = data.get('type', '')
#     message = data.get('message', '')
#     if not type or not message:
#         return web.HTTPBadRequest(reason='Type and message are required')
#     session = yield from get_session(request)
#     with(yield from request.app['db']) as conn:
#         ins_query = models.notifications.insert().values(
#             team=team['id'],
#             author=session['user_id'],
#             type=type,
#             message=message,
#             creation_date=datetime.datetime.now()
#         )
#         if(yield from conn.execute(ins_query)):
#             return web.HTTPCreated()
#         else:
#             return web.HTTPBadRequest(reason='Error while saving')


@asyncio.coroutine
def create_notification(request, type, message, team_id):
    if not type:
        raise ValueError("type arg is required")
    if not message:
        raise ValueError("message arg is required")
    if not team_id:
        raise ValueError("team_id arg is required")

    session = yield from get_session(request)
    nf_data = {
            'team': team_id,
            'author': session['user_id'],
            'type': type,
            'message': message,
            'creation_date': datetime.datetime.now()
        }
    with(yield from request.app['db']) as conn:

        trans = yield from conn.begin()
        try:
            ins_query = models.notifications.insert().values(nf_data)

            try:
                res = yield from conn.execute(ins_query)
            except Exception as e:
                print(str(e))
                raise AssertionError('can not save notification')
            else:
                nf_data['id'] = (yield from res.first())[0]
                nf_data['creation_date'] = str(nf_data['creation_date'])
                usr_query = sa.select([models.users]).where(models.users.c.id == session['user_id'])
                usr_res = yield from conn.execute(usr_query)
                usr_res = yield from usr_res.first()
                nf_data['author'] = {
                    'id': usr_res['avatar'],
                    'first_name': usr_res['first_name'],
                    'last_name': usr_res['last_name'],
                    'avatar': usr_res['avatar']
                }

        except Exception:
            yield from trans.rollback()
        else:
            yield from trans.commit()
            return nf_data


@asyncio.coroutine
def users(request, **kwargs):
    with(yield from request.app['db']) as conn:
        query = sa.select([models.users])
        ret = yield from conn.execute(query)
        schema = schemas.UserSchema(many=True)
        result = schema.dump(list(ret))
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

    resp = web.WebSocketResponse()
    yield from resp.prepare(request)
    socket_name = team['slug']

    socket_list_exists = request.app['sockets'].get(socket_name, None)
    if not socket_list_exists:
        print('list of sockets is not exists, creating one')
        request.app['sockets'][socket_name] = []
    request.app['sockets'][socket_name].append(resp)
    print(len(request.app['sockets'][socket_name]))

    while not resp.closed:
        msg = yield from resp.receive()

        if msg.tp == MsgType.text:
            if msg.data == 'close':
                yield from resp.close()
                request.app['sockets'][socket_name].remove(resp)
                if len(request.app['sockets'][socket_name]) < 1:
                    del request.app['sockets'][socket_name]
            else:
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError:
                    pass
                else:
                    try:
                        c = yield from create_notification(request, data['type'], data['message'], team['id'])
                    except Exception as e:
                        print(str(e))
                    else:
                        for ws in request.app['sockets'][socket_name]:
                            ws.send_str(json.dumps(c))

        elif msg.tp == MsgType.close:
            request.app['sockets'][socket_name].remove(resp)
            if len(request.app['sockets'][socket_name]) < 1:
                del request.app['sockets'][socket_name]
            print('websocket connection closed')

        elif msg.tp == MsgType.error:
            print('ws connection closed with exception %s' % ws.exception())

    return ws
