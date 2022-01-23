import os
from pydantic import BaseModel
import uvicorn

from fastapi import Depends, FastAPI
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_socketio import SocketManager
from fastapi.encoders import jsonable_encoder

from schemas import BroadcastItem
from worker import scrap_task

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sio = SocketManager(app=app)

def redis_cache():
    return caches.get(CACHE_KEY)

@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend(os.getenv("REDIS", "redis://redis:6378"))
    caches.set(CACHE_KEY, rc)

@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()

@app.get("/")
async def main():
    return RedirectResponse("/docs")

@app.post("/broadcast")
async def broadcast(item: BroadcastItem):
    item_json = jsonable_encoder(item)
    print(item_json)
    await sio.emit(item_json['event'], item_json['data'])
    return item
"""
@app.get("/search")
async def search(title: str, cache: RedisCacheBackend = Depends(redis_cache)):
    site_manager = SiteManager(cache, sites=[Zerion(), Filman(), Ekino()])
    if await site_manager.exists_in_cache(title):
        return await site_manager.get_from_cache(title)

    responses = await site_manager.process(title=title)
    responses_json = [x.to_json() for x in responses]
    await site_manager.add_to_cache(title=title, data=responses_json)
    return responses
"""


"""async def scrap_sites(title, sid):
    site_manager = SiteManager(sites=[Zerion(), Filman(), Ekino()])
    responses = await site_manager.process(title=title)
    
    await send_data_to_broadcast(responses)"""




@sio.on('connect')
async def handle_client_start_event(sid, *args, **kwargs):
	print(f"{sid} polaczyl sie") 

@sio.on("disconnect")
async def handle_disconnect(sid, *args, **kwargs):
    print(f"{sid} sie rozlaczyl")

@sio.on("search")
async def search(sid, data):
    scrap_task.apply_async(args=[data['title']])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)