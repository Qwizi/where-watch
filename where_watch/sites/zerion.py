import json
import httpx
from bs4 import BeautifulSoup
from sites.site import SiteMixin, SiteResponse, SiteResponseData
from fastapi_cache.backends.redis import RedisCacheBackend

class Zerion(SiteMixin):
    name = "zerion.cc"
    base_url = "https://zerion.cc"

    async def search(self, title: str) -> SiteResponseData:
        try:
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/szukaj?query={title}")
                html = BeautifulSoup(response.text, features="html.parser")
                title = self.clear_str(title)
                ul_list = html.find("ul", id="list")
                if not ul_list:
                    return self.not_found_response()
                urls = []
                for litag in ul_list.find_all("li"):
                    div_info = litag.find("div", class_="info")
                    if div_info:
                        h2_title = div_info.find("h2", class_="title")
                        h2_title_text = self.clear_str(h2_title.text)
                        print(title)
                        if title in h2_title_text:
                            url = div_info.find("a")['href']
                            urls.append(url)

                response.raise_for_status()
                response_data_dataclass = self.prepere_urls(urls)
                site_response = SiteResponse(name=self.name, base_url=self.base_url, data=response_data_dataclass)
                return site_response
        except (httpx.HTTPError) as e:
            return self.not_found_response()

        