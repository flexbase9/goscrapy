from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import sys
reload(sys)


class CommonSpider(CrawlSpider):
    
    name = "common"
    download_delay = 1
    allowed_domains = {"vsportss.com"}
    current = ''
    start_urls = [
        "http://www.vsportss.com/"
        ]
    
    def __init__(self, target=None):
        if self.current is not '':
            target = self.current
        if self.current is not None:
            self.current = target
        super(CommonSpider,self).__init__()
        