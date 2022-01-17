from bs4 import BeautifulSoup
import httpx
from sites.site import SiteMixin, SiteResponse, SiteResponseData
from fastapi_cache.backends.redis import RedisCacheBackend

class Filman(SiteMixin):
    name = "filman.cc"
    base_url = "https://filman.cc"

    async def search(self, title: str) -> SiteResponseData:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/wyszukiwarka?phrase={title}")
                html = BeautifulSoup(response.text, features="html.parser")
                search_div = html.find("div", id="advanced-search")
                title = self.clear_str(title)
                
                urls = []
                for row_div in search_div.find_all("div", class_="col-sm-4"):
                    title_div = row_div.find("div", class_="title")
                    if title_div:
                        title_div_text = self.clear_str(title_div.text)
                        if title in title_div_text:
                            url = row_div.find("a")['href']
                            urls.append(url)
                response.raise_for_status()
                response_data = self.prepere_urls(urls)
                return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)
        except httpx.HTTPError as e:
            return self.not_found_response()
    