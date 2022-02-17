from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .sites_crawler import Zerion


def run_zerion():
    process = CrawlerProcess(get_project_settings())
    process.crawl(Zerion)
    process.start(stop_after_crawl=False)
