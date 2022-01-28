from schemas import BroadcastItem
from sites.ekino import Ekino
from sites.filman import Filman
from sites.site import SiteManager
from sites.zerion import Zerion
from utils import send_data_to_broadcast


async def scrap_sites(title, sid):
    site_manager = SiteManager(sites=[Zerion(), Filman(), Ekino()])
    sites_data = await site_manager.process(title=title)
    broadcast_item = BroadcastItem(
        event="search_data", data=sites_data, sid=sid)
    await send_data_to_broadcast(broadcast_item)
