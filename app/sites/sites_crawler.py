import json
import scrapy
import requests


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

        data = {
            'title_eng': title,
            'title': title,
            'poster': poster,
            'site_url': 'https://zerion.cc',
            'site_link': url
        }
        response = requests.post(
            "http://app:8006/sites/process/", json=json.dumps(data))
        print(response.data)
