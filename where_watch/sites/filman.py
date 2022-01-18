from typing import List
from sites.site import SiteMixin, SiteResponse, SiteResponseData
class Filman(SiteMixin):
    """
    Site Filman.cc
    """
    name = "filman.cc"
    base_url = "https://filman.cc"

    async def find_urls(self, title, search_div) -> List[str]:
        # declare empty urls list
        urls = []
        # iterate over row div in search_div
        for row_div in search_div.find_all("div", class_="col-sm-4"):
            # get title div
            title_div = row_div.find("div", class_="title")

            # if title div not found continue
            if not title_div:
                continue

            # clear title_div text
            title_div_text = self.clear_str(title_div.text)
            
            # title not in title_div_text continue
            if title not in title_div_text:
                continue
            
            # find url in div_row
            url = row_div.find("a")['href']

            # if url not found continue
            if not url:
                continue

            # add url to urls list
            urls.append(url)
        return urls


    async def search(self, title: str) -> SiteResponseData:
        # Create url https://filman.cc/wyszukiwarka?phrase={title}
        url = f"{self.base_url}/wyszukiwarka?phrase={title}"
        # Get response
        html = await self.get_response_html(url)

        # if html is none return None
        if not html:
            return None

        # clear title
        title = self.clear_str(title)

        # Finding search div
        search_div = html.find("div", id="advanced-search")

        # If search div not found return None
        if not search_div:
            return None
        
        # find urls 
        urls = await self.find_urls(title, search_div)

        # if urls in empty return None
        if not urls:
            return None

        # site url data
        site_urls_data = self.prepere_urls(urls)
        # Return response
        return SiteResponse(name=self.name, base_url=self.base_url, data=site_urls_data)
