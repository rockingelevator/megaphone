import aiohttp
import aiohttp_jinja2
from aiohttp import web
from src.auth.users_auth import verify_password

@aiohttp_jinja2.template('home.jinja2')
async def home(request):
    return {}

@aiohttp_jinja2.template('login.jinja2')
async def login(request):
    if request.method == 'GET':
        return {}
    elif request.method == 'POST':
        check = await verify_password(request)
        if not check['error'] and check['verified']:
            return {'result': 'Verified!'}
        else:
            return check # return dict with error key



@aiohttp_jinja2.template('notifications.jinja2')
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


