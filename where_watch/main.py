from fastapi import FastAPI

from sites.site import SiteManager
from sites.zerion import Zerion
from sites.filman import Filman

app = FastAPI()

site_manager = SiteManager(sites=[Zerion(), Filman()])

@app.get("/search")
async def search(title: str):
    responses = await site_manager.process(title=title)
    return responses