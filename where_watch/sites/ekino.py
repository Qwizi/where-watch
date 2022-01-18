from typing import List
from sites.site import SiteMixin, SiteResponse, SiteResponseData
class Ekino(SiteMixin):
    """
    Ekino site
    """
    name = "ekino-tv"
    base_url = "https://ekino-tv.pl"

    async def find_urls(self, title, movie_wrap) -> List[str]:
        # declare empty urls list
        urls = []

        # itreate over row_div in movie_wrap
        for row_div in movie_wrap.find_all("div", class_="movies-list-item"):
            # Get title div
            title_div = row_div.find("div", class_="title")

            # If title div not found continue
            if not title_div:
                continue

            # Clear title div text
            title_div_text =  self.clear_str(title_div.text)

            # if title not in title_div_text continue
            if title not in title_div_text:
                continue

            # find url in div row
            url = row_div.find("a")['href']

            # if url not found continue
            if not url:
                continue

            # fix url path
            url = f"{self.base_url}{url}"
            
            # add url to url list
            urls.append(url)
        return urls

    async def search(self, title: str) -> SiteResponseData:
        # Create url https://ekino-tv.pl/search/qf/?q={title}
        url = f"{self.base_url}/search/qf/?q={title}"

        # Get response
        html = await self.get_response_html(url)

        # if html is none return None
        if not html:
            return None

        # clear title
        title = self.clear_str(title)

        # Finding movie wrap
        movie_wrap = html.find("div", class_="col-md-12 movie-wrap")

        # if movie wrap not found return none
        if not movie_wrap:
            return None
        
        # find urls
        urls = await self.find_urls(title, movie_wrap)

        # if urls is empty return None
        if not urls:
            return None

        # site data url
        site_urls_data = self.prepere_urls(urls)
        # Return response
        return SiteResponse(name=self.name, base_url=self.base_url, data=site_urls_data)
