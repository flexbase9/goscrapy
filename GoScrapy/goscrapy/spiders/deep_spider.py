# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from goscrapy.model.config import DBSession,response_output
from goscrapy.model.rule import Regular
from goscrapy.model.item import Item as ItemData


class Item(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    special = scrapy.Field()
    options = scrapy.Field()
    main_image_link = scrapy.Field()
    multiple_images_link = scrapy.Field()
    category = scrapy.Field()
    images_path = scrapy.Field()
    download = scrapy.Field()
    main_images = scrapy.Field()
    sku = scrapy.Field()
    parent_url = scrapy.Field()
    from_url = scrapy.Field()


class DeepSpider(CrawlSpider):
    name = "Deep"
    
    def __init__(self, site_name):
        self.db = DBSession()
        rule = self.db.query(Regular).filter(Regular.name == site_name).first()
        self.site_name = site_name
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page.split(','))))
        rule_list.append(Rule(LinkExtractor(allow=rule.allow_url.split(','), restrict_xpaths=rule.extract_from.split(',')), callback="parse_item"))
        self.rules = tuple(rule_list)
        super(DeepSpider, self).__init__()
        self.count = 0
        
    def make_requests_from_url(self, url):
        item = Item()
        
        item['parent_url'] = url
        request = Request(url, dont_filter=True)
        
        request.meta['item'] = item
        return request
        
    def parse_item(self, response):
        self.count += 1
        item = Item()
        _item = self.db.query(ItemData).filter(ItemData.from_url == response.url).first()
        if not _item:
            _i = ItemData(from_url=response.url)
            self.db.add(_i)
            self.db.commit()
        response.meta['rule'] = self.rule
        item = set_deep_item(item, response)
        
        print 'Crawled Url (Total:%s): %s' % (self.count, response.url)    
        return item        

def set_deep_item(item,response):
        item['from_url'] = response.url
        rule=response.meta['rule']
        
        item['parent_url'] = response.request.headers.get('referer',None)
        
        item['name'] = response_output(rule.name_xpath,response)             
        
        item['description'] = response_output(rule.description_xpath,response)             
        
        item['price'] = response_output(rule.price_xpath,response)       
        
        item['special'] = response_output(rule.special_xpath,response)                  
        
        item['options'] = response_output(rule.options_xpath,response)                       
        
        item['main_image_link'] = response_output(rule.main_image_link_xpath,response)                     
        
        item['multiple_images_link'] = response_output(rule.multiple_images_link_xpath,response)                  
        
        item['category'] = response_output(rule.category_xpath, response)                
        
        item['images_path'] = response_output(rule.images_path,response)                 
        
        item['download'] = rule.download if rule.download else 0                    
        
        item['sku'] = response_output(rule.sku_xpath,response)
            
        return item

def test_deep_item(response,site_name):
    item=Item()
    db=DBSession()
    rule = db.query(Regular).filter(Regular.name == site_name).first()
    response.meta['rule'] = rule
    print '%s' % set_deep_item(item, response)
    
