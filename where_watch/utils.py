import httpx
from schemas import BroadcastItem
from fastapi.encoders import jsonable_encoder

async def send_data_to_broadcast(item: BroadcastItem):
    item_json = jsonable_encoder(item)
    async with httpx.AsyncClient() as client:
        await client.post("http://where_watch:8006/broadcast", json=item_json)