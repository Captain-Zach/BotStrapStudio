import asyncio
import os
from aiohttp import web
import aiohttp
import aiohttp.web_ws
import aiohttp_cors

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

@routes.post('/login')
async def login(request):
    try:
        data = await request.json()
    except Exception:
        data = await request.post()
    username = data.get('username')
    password = data.get('password')
    # Simple hardcoded check (replace with real user validation)
    if username == 'admin' and password == 'password123':
        return web.json_response({'success': True, 'message': 'Login successful'})
    else:
        return web.json_response({'success': False, 'message': 'Invalid credentials'}, status=401)

@routes.post('/dashboard')
async def dashboard(request):
    try:
        data = await request.json()
    except Exception:
        data = await request.post()
    game = data.get('game')
    # For now, just acknowledge the game selection
    return web.json_response({'success': True, 'game': game})

def main():
    ssl_context = None  # Cloud Run manages HTTPS
    app = web.Application()
    app.add_routes(routes)

    # Enable CORS for localhost and production frontend
    cors = aiohttp_cors.setup(app, defaults={
        "http://localhost:5500": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
        "http://127.0.0.1:5500": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
        "https://hypergenesis.one": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
        "https://www.hypergenesis.one": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
        "*": aiohttp_cors.ResourceOptions()
    })
    for route in list(app.router.routes()):
        cors.add(route)

    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port, ssl_context=ssl_context)

if __name__ == '__main__':
    main()
