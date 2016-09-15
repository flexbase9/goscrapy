# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request


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
    main_image = scrapy.Field()
    multiple_image = scrapy.Field()
    sku = scrapy.Field()
    parent_url = scrapy.Field()
    from_url = scrapy.Field()


class DeepSpider(CrawlSpider):
    name = "Deep"
    
    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page.split(','))))
        rule_list.append(Rule(LinkExtractor(allow=[rule.allow_url.split(',')], restrict_xpaths=[rule.extract_from.split(',')]), callback="parse_item"))
        self.rules = tuple(rule_list)
        super(DeepSpider, self).__init__()
    
    def make_requests_from_url(self, url):
        item = Item()
        
        item['parent_url'] = url
        request= Request(url,dont_filter=True)
        
        request.meta['item'] = item
        return request
        
    def parse_item(self, response):
        self.log('Hi,This is an item list page!%s' % response.url)
        
        item = Item()
        
        
        item['parent_url'] = response.meta['item']['parent_url']
        item['from_url'] = response.url
        
        name = response.xpath(self.rule.name_xpath).extract()
        item['name'] = name[0] if name else ''                    
        
        description = response.xpath(self.rule.description_xpath).extract()
        item['description'] = description[0] if description else ''                    
        
        price = response.xpath(self.rule.price_xpath).extract()
        item['price'] = price[0] if price else ''                    
        
        special = response.xpath(self.rule.special_xpath).extract()
        item['special'] = special[0] if special else ''                    
        
        options = response.xpath(self.rule.options_xpath).extract()
        item['options'] = options[0] if options else ''                    
        
        main_image_link = response.xpath(self.rule.main_image_link_xpath).extract()
        item['main_image_link'] = main_image_link[0] if main_image_link else ''                    
        
        multiple_images_link = response.xpath(self.rule.multiple_images_link_xpath).extract()
        item['multiple_images_link'] =','.join([mi for mi in multiple_images_link if mi])                  
        
        category = response.xpath(self.rule.category_xpath).extract()
        item['category'] =','.join([ca for ca in category if ca])                    
        
        item['images_path'] = self.rule.images_path_xpath if self.rule.images_path_xpath else ''                    
        
        item['download'] = self.rule.download_xpath if self.rule.download else 0                    
        
                
        sku = response.xpath(self.rule.sku_xpath.extract())
        item['sku'] = sku[0] if sku else ''    
                      
        return item        
