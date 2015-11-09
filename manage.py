import asyncio
import aiohttp_debugtoolbar
from src.app import app

aiohttp_debugtoolbar.setup(app, intercept_redirects=False)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, '127.0.0.1', 8080)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(handler.finish_connections(1.0))
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.finish())
loop.close()





