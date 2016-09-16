from goscrapy.items import DmozItem
import scrapy

class DmozSpider(scrapy.Spider):
    name="dmoz"
    download_delay=1
    allowed_domains={"dmoz.org"}
    start_urls=[
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"
        ]

    def parse(self,response):
        for href in response.xpath('//a/@href'):
            url=response.urljoin(href.extract())
            yield scrapy.Request(url,callback=self.parse_contents)
    
    def parse_contents(self,response):
        for site in response.css('.site-item'):
            item=DmozItem()
            item['title']=site.css('.site-title').xpath('text()').extract()
            item['link']=site.xpath('.//a[@target]/@href').extract()
            item['desc']=site.css('.site-descr').xpath('text()').extract()
        yield item
        
        next_page=response.css()