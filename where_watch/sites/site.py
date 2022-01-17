from abc import abstractmethod
import asyncio
from dataclasses import dataclass
import json
from typing import List
from dataclasses_json import dataclass_json
from fastapi_cache.backends.redis import RedisCacheBackend
@dataclass
class Site:
    name: str
    url: str

@dataclass
class SiteResponseData:
    url: str

@dataclass_json
@dataclass
class SiteResponse:
    name: str
    base_url: str
    data: List[SiteResponseData]

class SiteMixin:
    base_url: str
    name: str

    @abstractmethod
    async def search(self, title: str) -> SiteResponseData:
        pass

    def not_found_response(self):
        return None

    def clear_str(self, string: str) -> str:
        return string.lower().replace(" ", "")

    def prepere_urls(self,urls: list[str]) -> List[SiteResponseData]:
        urls_to_response = []
        for url in urls:
            urls_to_response.append(SiteResponseData(url=url))
        return urls_to_response


class SiteManager:
    sites = List[SiteMixin]

    def __init__(self, cache, sites: List[SiteMixin]):
        self.cache: RedisCacheBackend = cache
        self.sites = sites

    
    async def process(self, title: str) -> List[SiteResponseData]:
        site_responses = await asyncio.gather(*[site.search(title=title) for site in self.sites])
            
        return [i for i in site_responses if i]

    async def get_sites(self) -> List[SiteMixin]:
        return self.sites

    async def get_cache_key(self, title: str) -> str:
        return str(f"search_{title}")

    async def exists_in_cache(self, title: str) -> bool:
        cache_key = await self.get_cache_key(title)
        return await self.cache.get(cache_key)

    async def add_to_cache(self, title: str, data: SiteResponse):
        if not await self.exists_in_cache(title):
            cache_key = await self.get_cache_key(title)
            data = json.dumps(data)
            await self.cache.set(cache_key, data, expire=5)
    
    async def get_from_cache(self, title):
        if await self.exists_in_cache(title):
            data = await self.cache.get(await self.get_cache_key(title))
            data = json.loads(data)
            converted_data = []
            for d in data:
                d = json.loads(d)
                converted_data.append(SiteResponse(**d))
            return converted_data
        return None