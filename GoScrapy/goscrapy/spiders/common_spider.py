# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from ..model.database import db_session
from ..model.config import response_output
#from ..model.rule import Regular
from ..model.item import Item as ItemData
from ..model.regular import Regular
import time
import re

class ItemValue(scrapy.Item):
    field = scrapy.Field()
    value = scrapy.Field()
    

class Item(scrapy.Item):
    site_name=scrapy.Field()
    parent_url = scrapy.Field()
    from_url = scrapy.Field()
    
    fields = scrapy.Field()


class CommonSpider(CrawlSpider):
    name = "Common"
    
    def __init__(self, site_name):
        self.db = db_session
        rule = Regular(name=site_name)
        self.site_name = site_name
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page.split(','))))
        rule_list.append(Rule(LinkExtractor(allow=rule.allow_url.split(','), restrict_xpaths=rule.extract_from.split(',')), callback="parse_item", process_request="process_request"))
        self.rules = tuple(rule_list)
        self.count = 0
        super(CommonSpider, self).__init__()
    
    def set_crawler(self, crawler):
        super(CommonSpider, self).set_crawler(self, crawler)
        
        
    def make_requests_from_url(self, url):
        item = Item()
        request = Request(url, dont_filter=True)
        
        request.meta['item'] = item
        return request
        
    def parse_item(self, response):
        item = Item()
        allow_urls = self.rule.allow_url.split(',')
        check_result=False
        for _urls_pattern in allow_urls:
            check=re.findall(_urls_pattern, response.url)
            check_result = check_result or check
        if check_result:    
            _item = self.db.query(ItemData).filter(ItemData.from_url == response.url).first()
            if not _item:
                _i = ItemData(from_url=response.url,site_name=self.name)
                self.db.add(_i)
                self.db.commit()
            response.meta['rule'] = self.rule
            item = set_common_item(item, response)
            slap_time = (time.time() - self.settings['START_TIME']) / 60
            self.count += 1
            print 'Crawled Url (Total:%s - %d Minute): %s' % (self.count, slap_time, response.url)    
            return item  
        else:
            return None 
    
    def process_request(self, request):
        new_url = request.url
        string = self.rule.filter_url
        if string:
            string = string.replace('\,', '~~~~~').replace('\:', '!!!!!')
            groups = string.split(',')
            for g in groups:
                _g = g.split(':')
                if len(_g) == 2:
                    new_url = re.sub(_g[0].replace('~~~~~', ',').replace('!!!!!', ':'), _g[1].replace('~~~~~', ',').replace('!!!!!', ':'), new_url)
                elif len(_g) == 1:
                    new_url = re.sub(_g[0].replace('~~~~~', ',').replace('!!!!!', ':'), '', new_url)
        request = request.replace(url=new_url)
        return request

def set_common_item(item, response):
        item['from_url'] = response.url
        rule = response.meta['rule']
        
        item['parent_url'] = response.request.headers.get('referer', None)
        
        item['site_name'] =rule.name
        
        parse_setting = rule.get_parse_setting()
        
        item_values=list()
        for ps in parse_setting:
            item_value=ItemValue()
            item_value['field']=ps.field_to
            item_value['value']=response_output(ps.value, response)
            item_values.append(item_value)
        item['fields']=item_values
        return item

def test_item(response, site_name):
    item = Item()
    rule = Regular(name=site_name)
    response.meta['rule'] = rule
    print '%s' % set_common_item(item, response)
    
