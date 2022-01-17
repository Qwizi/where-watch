from fastapi import Depends, FastAPI
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from fastapi.middleware.cors import CORSMiddleware


from sites.site import SiteManager, SiteResponse
from sites.zerion import Zerion
from sites.filman import Filman
from sites.ekino import Ekino

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def redis_cache():
    return caches.get(CACHE_KEY)


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend('redis://localhost:6379')
    caches.set(CACHE_KEY, rc)

@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


@app.get("/search")
async def search(title: str, cache: RedisCacheBackend = Depends(redis_cache)):
    site_manager = SiteManager(cache, sites=[Zerion(), Filman(), Ekino()])
    if await site_manager.exists_in_cache(title):
        print("Pobieram z cache")
        return await site_manager.get_from_cache(title)
    print("Cache nie istnieje")

    responses = await site_manager.process(title=title)
    responses_json = []
    for r in responses:
        responses_json.append(r.to_json())
    await site_manager.add_to_cache(title=title, data=responses_json)
    return responses