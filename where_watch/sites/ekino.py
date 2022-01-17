from bs4 import BeautifulSoup
import httpx
from sites.site import SiteMixin, SiteResponse, SiteResponseData
from fastapi_cache.backends.redis import RedisCacheBackend

class Ekino(SiteMixin):
    name = "ekino-tv"
    base_url = "https://ekino-tv.pl"

    async def search(self, title: str) -> SiteResponseData:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/search/qf/?q={title}")
                html = BeautifulSoup(response.text, features="html.parser")
                title = self.clear_str(title)
                urls = []

                search_div = html.find("div", class_="col-md-12 movie-wrap")
                for row_div in search_div.find_all("div", class_="movies-list-item"):
                    title_div = row_div.find("div", class_="title")
                    if title_div:
                        title_div_text = self.clear_str(title_div.text)
                        if title in title_div_text:
                            url = row_div.find("a")['href']
                            url = f"{self.base_url}{url}"
                            urls.append(url)            
                response.raise_for_status()
                if not urls:
                    return None
                response_data = self.prepere_urls(urls)
                return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)
        except httpx.HTTPError as e:
            return None
    