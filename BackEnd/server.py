import asyncio
import ssl
import os
from aiohttp import web
import aiohttp
import aiohttp.web_ws
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Paths to SSL certificate and key (now loaded from .env file)
SSL_CERT_PATH = os.environ.get('SSL_CERT_PATH', 'domain.cert.pem')
SSL_KEY_PATH = os.environ.get('SSL_KEY_PATH', 'private.key.pem')

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
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8443, ssl_context=ssl_context)

if __name__ == '__main__':
    main()
