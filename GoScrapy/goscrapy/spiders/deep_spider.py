# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from goscrapy.model.config import DBSession
from goscrapy.model.rule import Regular
import re
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
        db = DBSession()
        rule = db.query(Regular).filter(Regular.name == site_name).one()
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
    
    def make_requests_from_url(self, url):
        item = Item()
        
        item['parent_url'] = url
        request = Request(url, dont_filter=True)
        
        request.meta['item'] = item
        return request
        
    def parse_item(self, response):
        
        item = Item()
        
        
        # item['parent_url'] = response.meta['item']['parent_url']
        item['from_url'] = response.url
        
        name = response.xpath(self.rule.name_xpath).extract()
        item['name'] = (name[0] if name else '').strip(" \t\n\r")               
        
        description = response.xpath(self.rule.description_xpath).extract()
        item['description'] = (description[0] if description else '').strip(" \t\n\r")                    
        
        price = response.xpath(self.rule.price_xpath).extract()
        format_price = re.findall("\d+\.?\d+", price[0] if price else '')  
        item['price'] = (format_price if format_price else [''])[0]             
        
        special = response.xpath(self.rule.special_xpath).extract()
        format_special = re.findall("\d+\.?\d+", special[0] if special else '') 
        item['special'] = (format_special if format_special else [''])[0]                   
        
        options = response.xpath(self.rule.options_xpath).extract()
        item['options'] = ','.join([op for op in options if op])                    
        
        main_image_link = response.xpath(self.rule.main_image_link_xpath).extract()
        item['main_image_link'] = (main_image_link[0] if main_image_link else '').strip(" \t\n\r")                    
        
        multiple_images_link = response.xpath(self.rule.multiple_images_link_xpath).extract()
        item['multiple_images_link'] = (','.join([mi for mi in multiple_images_link if mi])).strip(" \t\n\r")                  
        
        category = response.xpath(self.rule.category_xpath).extract()
        item['category'] = ','.join([ca for ca in category if ca])                    
        
        item['images_path'] = self.rule.images_path if self.rule.images_path else ''                    
        
        item['download'] = self.rule.download if self.rule.download else 0                    
        
        sku = response.xpath(self.rule.sku_xpath).extract()
        item['sku'] = (sku[0] if sku else '').strip(" \t\n\r")               
        return item        
