import asyncio
import aiohttp_jinja2
import sqlalchemy as sa
from aiohttp import web
from aiohttp_session import get_session
from src.auth.users_auth import verify_password
from src import models



def redirect_if_not_logged_in(fn):
    """
    Decorator for handlers, redirects to login page if user is not signed in
    """
    async def check_auth(request):
        session = await get_session(request)
        if not 'user_id' in session:
            return web.HTTPFound(request.app.router['login'].url())
        else:
            return (await fn(request))
    return check_auth

def check_if_user_in_team(handler):
    @asyncio.coroutine
    def check(request):
        url_to_login = request.app.router['login'].url()
        session = yield from get_session(request)
        if not 'user_id' in session:
            print('Team is not allowed, sign in first')
            return web.HTTPFound(url_to_login)
        team_slug = request.match_info['team_slug']
        with (yield from request.app["db"]) as conn:
            team_query = sa.select([models.teams]).where(models.teams.c.slug==team_slug)
            select_team = yield from conn.execute(team_query)
            team = yield from select_team.first()
            if not team:
                return web.HTTPNotFound()
            else:
                relation_query = sa.select([models.teams_users])\
                    .where(sa.and_(models.teams_users.c.team==team['id'],
                           models.teams_users.c.user==session['user_id']))
                find_relation = yield from conn.execute(relation_query)
                rel = yield from find_relation.first()
                if not rel:
                    return web.HTTPNotFound()# user is not in this team, return 404
                return (yield from handler(request, team))
    return check


@aiohttp_jinja2.template('home.jinja2')
async def home(request):
    return {}

@aiohttp_jinja2.template('login.jinja2')
async def login(request):
    session = await get_session(request)
    redirect_url = request.app.router["notifications"].url(parts={
        'team_slug': 'demo-team'
    })
    if request.method == 'GET':
        if 'user_id' in session:
            print('redirecting to notifications')
            return web.HTTPFound(redirect_url)
        return {}
    elif request.method == 'POST':
        check = await verify_password(request)
        if not check['error'] and check['user_id']:
            session['user_id'] = check["user_id"]
            return web.HTTPFound(redirect_url)
        else:
            return check # return dict with error key


async def logout(request):
    session = await get_session(request)
    if 'user_id' in session: session.invalidate()
    return web.HTTPFound(request.app.router['login'].url())


@aiohttp_jinja2.template('notifications.jinja2')
@check_if_user_in_team
@asyncio.coroutine
def notifications(request, team):
    with(yield from request.app['db']) as conn:
        notif = models.notifications.alias()
        recent_notif_query = sa.select([notif])\
            .where(notif.c.team == team['id'])\
            .order_by(sa.desc(notif.c.creation_date))\
            .limit(20)
        n_list = yield from (yield from conn.execute(recent_notif_query)).fetchall()
    return {
        'team': team,
        'n_list': n_list
    }


# async def websocket_handler(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)
#
#     while not ws.closed:
#         msg = await ws.receive()
#
#         if msg.tp == aiohttp.MsgType.text:
#             if msg.data == 'close':
#                 await ws.close()
#             else:
#                ws.send_str(msg.data+'/answer')
#         elif msg.tp == aiohttp.MsgType.close:
#             print('websocket connection closed')
#         elif msg.tp == aiohttp.MsgType.error:
#             print('ws connection closed with exception %s' % ws.exception())
#
#     return ws


