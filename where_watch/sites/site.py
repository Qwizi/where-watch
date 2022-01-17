from abc import abstractmethod
import asyncio
from dataclasses import dataclass
from typing import List

@dataclass
class Site:
    name: str
    url: str

@dataclass
class SiteResponseData:
    url: str

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
        response_data = SiteResponseData(url=None)
        return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)

    def clear_str(self, string: str) -> str:
        return string.lower().replace(" ", "")


class SiteManager:
    sites = List[SiteMixin]

    def __init__(self, sites: List[SiteMixin]):
        self.sites = sites

    
    async def process(self, title: str) -> List[SiteResponseData]:
        site_responses = await asyncio.gather(*[site.search(title=title) for site in self.sites])
        return site_responses

    async def get_sites(self) -> List[SiteMixin]:
        return self.sites