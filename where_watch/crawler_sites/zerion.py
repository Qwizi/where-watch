import json
import httpx
import scrapy


class Zerion(scrapy.Spider):
    name = "zerion"
    start_urls = ["https://zerion.cc/seriale"]

    def parse(self, response):
        # xpath
        # title //div[@class='info']//h2[@class='title']/text()
        links = response.xpath("//a[@class='poster']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        url = kwargs.pop("url", None)
        title = response.xpath(
            "//div[@class='info']/h2[@class='title']/text()").get()
        poster = response.xpath("//div[@class='poster']/img/@src").get()
        poster = f'https://zerion.cc/{poster}'

        response = httpx.post("http://web:8006/process", data=json.dumps(
            {
                "title": title,
                "title_eng": title,
                "poster": poster,
                "site_url": "http://zerion.cc",
                "site_link": url
            }
        ))

        print(response.json())

        # yield {
        #    'url': url,
        #    'title': title,
        #    'poster': poster,
        # }
