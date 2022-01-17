from sites.site import SiteMixin, SiteResponse, SiteResponseData

class Filman(SiteMixin):
    name = "filman.cc"
    base_url = "https://filman.cc"

    async def search(self, title: str) -> SiteResponseData:
        response_data = SiteResponseData(url=title)
        return SiteResponse(name=self.name, base_url=self.base_url, data=response_data)
    