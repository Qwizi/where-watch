import httpx
from bs4 import BeautifulSoup
from sites.site import SiteMixin, SiteResponse, SiteResponseData

class Zerion(SiteMixin):
    name = "zerion.cc"
    base_url = "https://zerion.cc"

    async def search(self, title: str) -> SiteResponseData:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/szukaj?query={title}")
                html = BeautifulSoup(response.text, features="html.parser")
                ul_list = html.find("ul", id="list")
                title = title.lower().replace(" ", "")
                print(title)
                if not ul_list:
                    print(html.prettify())
                    response_data = SiteResponseData(url=None)
                    return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)
                url = None
                for litag in ul_list.find_all("li"):
                    div_info = litag.find("div", class_="info")
                    if div_info:
                        h2_title = div_info.find("h2", class_="title")
                        h2_title_text = h2_title.text.lower().replace(" ", "")
                        if title in h2_title_text:
                            url = div_info.find("a")['href']
                            break

                response.raise_for_status()
                response_data = SiteResponseData(url=url)
                return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)
        except (httpx.HTTPError) as e:
            response_data = SiteResponseData(url=None)
            return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)

        