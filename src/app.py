import asyncio
from aiohttp_debugtoolbar import toolbar_middleware_factory
import aiohttp_jinja2, jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import src.handlers as handlers
import settings as settings
from aiopg.sa import create_engine
from src.api import handlers as api_handlers

# db middleware
@asyncio.coroutine
def db_middleware(app, handler):
    @asyncio.coroutine
    def middleware(request):
        db = app.get('db')
        if not db:
            app['db'] = db = yield from create_engine(app['dsn'])
        request.app['db'] = db
        return (yield from handler(request))
    return middleware


# app initialization
app = web.Application(middlewares=[
    db_middleware,
    toolbar_middleware_factory,
    session_middleware(EncryptedCookieStorage(settings.SECRET_KEY))
])

# db settings
app['dsn'] = settings.DSN

# configuring path to templates
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# configuring path for static files
app.router.add_static('/static', 'static', name='static')

# ROUTES
app.router.add_route('GET', '/', handlers.home)
app.router.add_route('GET',
                     '/{team_slug}/notifications',
                     handlers.notifications,
                     name="notifications"
                     )
app.router.add_route('GET', '/login', handlers.login, name="login")
app.router.add_route('POST', '/login', handlers.login, name="submit_login")
app.router.add_route('GET', '/logout', handlers.logout, name="logout")
#API routes
app.router.add_route('GET', '/api/{team_slug}/notifications', api_handlers.notifications, name="api.notifications")
