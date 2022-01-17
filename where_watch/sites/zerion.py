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
                    return None
                urls = []
                for litag in ul_list.find_all("li"):
                    div_info = litag.find("div", class_="info")
                    if div_info:
                        h2_title = div_info.find("h2", class_="title")
                        h3_title = div_info.find("h3", class_="title-original")
                        if h2_title:
                            h2_title_text = self.clear_str(h2_title.text)
                            if title in h2_title_text:
                                url = div_info.find("a")['href']
                                if url:
                                    urls.append(url)
                        if h3_title:
                            h3_title_text = self.clear_str(h3_title.text)
                        
                            if title in h3_title_text:
                                url = div_info.find("a")['href']
                                if url:
                                    urls.append(url)

                response.raise_for_status()
                if not urls:
                    return None
                site_response = self.prepere_urls(urls)
                return SiteResponse(name=self.name, base_url=self.base_url, data=site_response)
        except (httpx.HTTPError, AttributeError) as e:
            print(e)
            return None


        