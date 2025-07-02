import asyncio
import os
from aiohttp import web
import aiohttp
import aiohttp.web_ws

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    return web.Response(text="Backend server is running (HTTPS & WSS enabled)")

@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await ws.send_str(f"Echo: {msg.data}")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'WebSocket connection closed with exception {ws.exception()}')
    return ws

def main():
    ssl_context = None  # Cloud Run manages HTTPS
    app = web.Application()
    app.add_routes(routes)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port, ssl_context=ssl_context)

if __name__ == '__main__':
    main()
