import os
from typing import Optional
import aioredis
import uvicorn

from fastapi import Depends, FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_socketio import SocketManager
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from schemas import BroadcastItem
from worker import scrap_task

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sio = SocketManager(app=app)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.on_event('startup')
async def on_startup() -> None:
    redis = aioredis.from_url(
        "redis://redis:6378", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, title: Optional[str] = None):
    if title:
        print(title)
    return templates.TemplateResponse("index.html", {'request': request, "title": title})


@app.post("/broadcast")
async def broadcast(item: BroadcastItem):
    item_json = jsonable_encoder(item)
    print(item_json)
    await sio.emit(item_json['event'], item_json['data'], to=item_json['sid'])
    return item


@sio.on('connect')
async def handle_client_start_event(sid, *args, **kwargs):
    print(f"{sid} polaczyl sie")


@sio.on("disconnect")
async def handle_disconnect(sid, *args, **kwargs):
    print(f"{sid} sie rozlaczyl")


@sio.on("search")
async def search(sid, data):
    scrap_task.apply_async(args=[data['title'], sid])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
