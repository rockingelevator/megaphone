import aiohttp
import aiohttp_jinja2
from aiohttp import web
from src.auth.users_auth import verify_password
from aiohttp_session import get_session

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



@aiohttp_jinja2.template('home.jinja2')
async def home(request):
    return {}

@aiohttp_jinja2.template('login.jinja2')
async def login(request):
    session = await get_session(request)
    redirect_url = request.app.router["notifications"].url()
    if request.method == 'GET':
        if 'user_id' in session:
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
@redirect_if_not_logged_in
async def notifications(request):
    return {}

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


