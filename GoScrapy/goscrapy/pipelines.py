# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import json
import codecs
from model.config import DBSession
from model.config import Redis
from model.item import Item

class GoscrapyPipeline(object):
    def process_item(self, item, spider):
        return item
    
#Remove the duplicated items    
class DuplicatesPipeline(object):
    def process_item(self,item,spider):
        if Redis.exists('url:%s' % item['from_url']):
            raise DropItem("Duplicate item found:%s" % item)
        else:
            Redis.set('url:%s' % item['from_url'],1)
            return item
        
class DataBasePipeline(object):
    def open_spider(self,spider):
        self.session=DBSession()
        
    def process_item(self,item,spider):
        i=Item(name=item['name'].encode('utf-8'),description = item['description'].encode('utf-8'),price = item['price'].encode('utf-8'),
               special = item['special'].encode('utf-8'),options = item['options'].encode('utf-8'),main_image_link = item['main_image_link'].encode('utf-8'),
               multiple_images_link = item['multiple_images_link'].encode('utf-8'),category = item['category'].encode('utf-8'),images_path = item['images_path'].encode('utf-8'),
               download = item['download'].encode('utf-8'),main_image = item['main_image'].encode('utf-8'),multiple_image = item['multiple_image'].encode('utf-8'),
               sku=item['sku'].encode('utf-8'),from_url = item['from_url'].encode('utf-8'))
        self.session.add(i)
        self.session.commit()
        
    def close_spider(self,spider):
        self.session.close()


class SaveImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        all_images_links=[ url for url in (item['main_image_link'].split(",") + item['multiple_images_link'].split(",")) if url !="" ] 
        for image_url in all_images_links:
            yield Request(image_url)
            
    def item_completed(self, results, item, info):
        image_paths=[x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['main_image']=image_paths
        return item
    
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)


class JsonWriterPipeline(object):
    
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding = 'utf-8')
        
    def process_item(self,item,spider):
        line = json.dump(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item
    
class CountDropPipeline(object):
    def __init__(self):
        self.count=100
        
    def process_item(self,item,spider):
        if self.count == 0:
            raise DropItem("Over item found: %s" % item)
        else:
            self.count -=1
            return item
        
        