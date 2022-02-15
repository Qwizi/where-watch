import datetime
import os
import time
from typing import List, Optional
import aioredis
import databases
import sqlalchemy
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
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from schemas import BroadcastItem, SeriesProcess
from models import Series, Site, SiteLink
from schemas import SeriesPydantic, SiteLinkPydantic, SitePydantic
from db import init_db
from worker import run_crawler, scrap_task

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
    init_db(app)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, title: Optional[str] = None):
    if title:
        print(title)
    return templates.TemplateResponse("index.html", {'request': request, "title": title})


@app.get("/sites", response_model=List[SitePydantic])
async def sites():
    return await SitePydantic.from_queryset(Site.all())


@app.get("/series", response_model=List[SeriesPydantic])
async def series():
    return await SeriesPydantic.from_queryset(Series.all())


@app.get("/series/{series_id}", response_model=SeriesPydantic)
async def series_detail(series_id):
    query = await Series.filter(id=series_id).prefetch_related("links").first()

    print(await query.links.all())
    return await SeriesPydantic.from_tortoise_orm(query)


@app.get("/sitesl", response_model=List[SiteLinkPydantic])
async def series():
    query = SiteLink.all()
    return await SiteLinkPydantic.from_queryset(query)


@ app.get("/scrap")
async def scrap():
    run_crawler.delay("test")
    return True


@ app.post("/process")
async def process(process: SeriesProcess):
    site_url = process.site_url
    site_exists = await Site.filter(url=site_url).exists()
    site = None
    if site_exists:
        site = await Site.get(url=site_url)
        series = None
        if not await Series.filter(title=process.title).exists():
            series = await Series.create(
                title=process.title,
                title_eng=process.title_eng,
                poster=process.poster,
                premiere_date=datetime.datetime.now(),
                update_date=datetime.datetime.now()
            )
        else:
            series = await Series.get(title=process.title)

        site_link_exists = await SiteLink.filter(
            link=process.site_link, site=site).exists()

        site_link = None
        if not site_link_exists:
            site_link = await SiteLink.create(
                site=site,
                link=process.site_link
            )
        else:
            site_link = await SiteLink.get(site=site, link=process.site_link)

        await series.links.add(site_link)

        print(series.links.all())
    return process


@ app.post("/broadcast")
async def broadcast(item: BroadcastItem):
    item_json = jsonable_encoder(item)
    print(item_json)
    await sio.emit(item_json['event'], item_json['data'], to=item_json['sid'])
    return item


@ sio.on('connect')
async def handle_client_start_event(sid, *args, **kwargs):
    print(f"{sid} polaczyl sie")


@ sio.on("disconnect")
async def handle_disconnect(sid, *args, **kwargs):
    print(f"{sid} sie rozlaczyl")


@ sio.on("search")
async def search(sid, data):
    scrap_task.apply_async(args=[data['title'], sid])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
