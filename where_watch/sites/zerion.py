import json
from typing import List
import httpx
from bs4 import BeautifulSoup
from sites.site import SiteMixin, SiteResponse, SiteResponseData
from fastapi_cache.backends.redis import RedisCacheBackend

"""
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
        """

class Zerion(SiteMixin):
    """
    Site Zerion.cc
    """
    name = "zerion.cc"
    base_url = "https://zerion.cc"

    async def find_urls(self, title, ul_list) -> List[str]:
        # declare empty url list
        urls = []
        for litag in ul_list.find_all("li"):
            # get div info
            div_info = litag.find("div", class_="info")
            # if div info is not found return None
            if not div_info:
                continue
            
            # Polish title
            h2_title = div_info.find("h2", class_="title")
            # English title
            h3_title = div_info.find("h3", class_="title-original")

            # If h2_title and h3_title not found continue
            if not h2_title and not h3_title:
                continue

            # if h2 title found
            if h2_title:
                # clear h2 title text
                h2_title_text = self.clear_str(h2_title.text)

                if title in h2_title_text:
                    # find url in div_info
                    url = div_info.find("a")['href']
                    # if url not found continue
                    if not url:
                        continue
                    # else add url to urls list
                    urls.append(url)
            # if h2 title not found
            else:
                h3_title_text = self.clear_str(h3_title.text)

                if title in h3_title_text:
                    # find url in div_info
                    url = div_info.find("a")['href']
                    # if url not found continue
                    if not url:
                        continue
                    # else add url to urls list
                    urls.append(url)
        return urls

    async def search(self, title: str) -> SiteResponseData:
        try:
            #   https://zerion.cc/szukaj?query=asdsd
            url = f"{self.base_url}/szukaj?query={title}"
            # Get response
            html = await self.get_response_html(url)
        except httpx.HTTPError as e:
            print(e)
            # If HTTPError return none
            return None
        # clear title
        title = self.clear_str(title)
        # Finding ul with id is equal list
        ul_list = html.find("ul", id="list")
        # If list not found return None
        if not ul_list:
            return None

        # url list
        urls = await self.find_urls(title, ul_list)
        # if url list is empty return none
        if not urls:
            return None
        
        # site url data
        site_urls_data = self.prepere_urls(urls)
        # Return response
        return SiteResponse(name=self.name, base_url=self.base_url, data=site_urls_data)
