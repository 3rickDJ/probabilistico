from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import os

def scrap():
    if os.path.exists('items.json'):
        # return
        os.remove('items.json')
    process = CrawlerProcess(get_project_settings())
    process.crawl('quotes')
    process.start() # the script will block here until the crawling is finished
    items = json.load(open('items.json'))
    return items
