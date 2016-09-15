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
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page)))
        rule_list.append(Rule(LinkExtractor(allow=[rule.allow_url], restrict_xpaths=[rule.extract_from]), callback="parse_item"))
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
        
        name = response.xpath(self.rule.name_xpath.extract())
        item['name'] = name[0] if name else ''                    
        
        description = response.xpath(self.rule.description_xpath.extract())
        item['description'] = description[0] if description else ''                    
        
        price = response.xpath(self.rule.price_xpath.extract())
        item['price'] = price[0] if price else ''                    
        
        special = response.xpath(self.rule.special_xpath.extract())
        item['special'] = special[0] if special else ''                    
        
        options = response.xpath(self.rule.options_xpath.extract())
        item['options'] = options[0] if options else ''                    
        
        main_image_link = response.xpath(self.rule.main_image_link_xpath.extract())
        item['main_image_link'] = main_image_link[0] if main_image_link else ''                    
        
        multiple_images_link = response.xpath(self.rule.multiple_images_link_xpath.extract())
        item['multiple_images_link'] = multiple_images_link[0] if multiple_images_link else ''                    
        
        category = response.xpath(self.rule.category_xpath.extract())
        item['category'] = category[0] if category else ''                    
        
        images_path = response.xpath(self.rule.images_path_xpath.extract())
        item['images_path'] = images_path[0] if images_path else ''                    
        
        download = response.xpath(self.rule.download_xpath.extract())
        item['download'] = download[0] if download else ''                    
        
        main_image = response.xpath(self.rule.main_image_xpath.extract())
        item['main_image'] = main_image[0] if main_image else ''                    

        multiple_image = response.xpath(self.rule.multiple_image_xpath.extract())
        item['multiple_image'] = multiple_image[0] if multiple_image else ''  
                
        sku = response.xpath(self.rule.sku_xpath.extract())
        item['sku'] = sku[0] if sku else ''    
                      
        return item        
