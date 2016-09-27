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
from model.common_item import CommonItem, CommonItemLine
from model.database import db_session
from urlparse import urlparse
from sqlalchemy import update
import hashlib

class GoscrapyPipeline(object):
    def process_item(self, item, spider):
        return item
    
# Remove the duplicated items    
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('url:%s' % item['from_url']):
            raise DropItem("Duplicate item found:%s" % item)
        else:
            Redis.set('url:%s' % item['from_url'], 1)
            return item

class CommonDataBasePipeline(object):
    def open_spider(self, spider):
        self.session = db_session
        
    def process_item(self, item, spider):
        common_item = CommonItem.query.filter_by(from_url = item['from_url']).first()
        if common_item:
            for _item in common_item.items:
                self.session.delete(_item)
            self.session.commit()
        else:
            common_item = CommonItem()
            
        common_item.site_name = item['site_name'].encode('utf-8')
        common_item.from_url = item['from_url'].encode('utf-8')
        common_item.parent_url = item['parent_url'].encode('utf-8')
        for item_field in item['fields']:
            item_line = CommonItemLine()
            item_line.field = item_field['field'].encode('utf-8')
            item_line.value = item_field['value'].encode('utf-8')
            common_item.items.append(item_line)
        self.session.add(common_item)
        self.session.commit()
        
    def close_spider(self, spider):
        self.session.close()

class CommonSaveImagesPipeline(ImagesPipeline):
    
    def uri_validator(self, x):
        try:
            result = urlparse(x)
            return True if result.scheme else False
        except:
            return False
        
    def get_field_value(self, fields, field_name):
        if fields:
            for f in fields:
                if f['field'] == field_name:
                    return f['value']
        return ''
    
    def get_media_requests(self, item, info):
        
        main_image_link = self.get_field_value(item['fields'], u'main_image_link')
        multiple_images_link = self.get_field_value(item['fields'], u'multiple_images_link')
        
        all_images_links = set([ url for url in (main_image_link.split(",") + multiple_images_link.split(",")) if url != "" ])
        parsed_uri = urlparse(item['from_url'])
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        for image_url in all_images_links:
            if not self.uri_validator(image_url):
                image_url = domain + image_url
                
            name = self.get_field_value(item['fields'], u'name')
            images_path = self.get_field_value(item['fields'], u'images_path')
            
        
            yield Request(image_url, meta={'image_names':name, 'images_path':images_path, 'from_url':item['from_url']})
            
    def item_completed(self, results, item, info):
        image_paths = ['/'.join(x['path'].split('/')[1:]) for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['fields'].append({'field':'main_images' ,'value' :','.join(set(image_paths))})
        return item
    
    def file_path(self, request, response=None, info=None):
        parsed_uri = urlparse(request.meta['from_url'])
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        hashed_url = hashlib.md5(request.url)
        image_name = request.url.split('/')[-1]
        image_extension = request.url.split('.')[-1]
        if request.meta['image_names']:
            image_name = ''.join([a for a in request.meta['image_names'].replace(" ", "-").lower() if a.isalpha() or a.isdigit() or a == '-']) 
            image_name = image_name + "-" + ('%d' % int(hashed_url.hexdigest(), 16))[0:8] + '.' + image_extension
        path = '/images'
        if request.meta['images_path']:
            path = '/' + request.meta['images_path']
        return '%s%s/%s' % (domain, path, image_name)
    
    
class DataBasePipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()
        
    def process_item(self, item, spider):
        
        _item = self.session.query(Item).filter(Item.from_url == item['from_url']).first()
        if _item:
            ex = update(Item).where(Item.id == _item.id).values(id=_item.id, site_name=item['site_name'].encode('utf-8'), name=item['name'].encode('utf-8'), description=item['description'].encode('utf-8'), price=item['price'].encode('utf-8'),
               special=item['special'].encode('utf-8'), options=item['options'].encode('utf-8'), main_image_link=item['main_image_link'].encode('utf-8'),
               multiple_images_link=item['multiple_images_link'].encode('utf-8'), category=item['category'].encode('utf-8'), images_path=item['images_path'].encode('utf-8'),
               download=item['download'].encode('utf-8'), main_images=item['main_images'].encode('utf-8'), sku=item['sku'].encode('utf-8'), from_url=item['from_url'].encode('utf-8'), parent_url=item['parent_url'].encode('utf-8'))
            self.session.execute(ex)
        else:
            i = Item(name=item['name'].encode('utf-8'), site_name=item['site_name'].encode('utf-8'), description=item['description'].encode('utf-8'), price=item['price'].encode('utf-8'),
               special=item['special'].encode('utf-8'), options=item['options'].encode('utf-8'), main_image_link=item['main_image_link'].encode('utf-8'),
               multiple_images_link=item['multiple_images_link'].encode('utf-8'), category=item['category'].encode('utf-8'), images_path=item['images_path'].encode('utf-8'),
               download=item['download'].encode('utf-8'), main_images=item['main_images'].encode('utf-8'), sku=item['sku'].encode('utf-8'), from_url=item['from_url'].encode('utf-8'), parent_url=item['parent_url'].encode('utf-8'))
            self.session.add(i)
        self.session.commit()
        
    def close_spider(self, spider):
        self.session.close()
        
        
class SaveImagesPipeline(ImagesPipeline):
    
    def uri_validator(self, x):
        try:
            result = urlparse(x)
            return True if result.scheme else False
        except:
            return False
    
    def get_media_requests(self, item, info):
        
        all_images_links = set([ url for url in (item['main_image_link'].split(",") + item['multiple_images_link'].split(",")) if url != "" ])
        parsed_uri = urlparse(item['from_url'])
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        for image_url in all_images_links:
            if not self.uri_validator(image_url):
                image_url = domain + image_url
            yield Request(image_url, meta={'image_names':item['name'], 'images_path':item['images_path'], 'from_url':item['from_url']})
            
    def item_completed(self, results, item, info):
        image_paths = ['/'.join(x['path'].split('/')[1:]) for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['main_images'] = ','.join(set(image_paths))
        return item
    
    def file_path(self, request, response=None, info=None):
        parsed_uri = urlparse(request.meta['from_url'])
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        hashed_url = hashlib.md5(request.url)
        image_name = request.url.split('/')[-1]
        image_extension = request.url.split('.')[-1]
        if request.meta['image_names']:
            image_name = ''.join([a for a in request.meta['image_names'].replace(" ", "-").lower() if a.isalpha() or a.isdigit() or a == '-']) 
            image_name = image_name + "-" + ('%d' % int(hashed_url.hexdigest(), 16))[0:8] + '.' + image_extension
        path = '/images'
        if request.meta['images_path']:
            path = '/' + request.meta['images_path']
        return '%s%s/%s' % (domain, path, image_name)

class JsonWriterPipeline(object):
    
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')
        
    def process_item(self, item, spider):
        line = json.dump(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item
    
class CountDropPipeline(object):
    def __init__(self):
        self.count = 100
        
    def process_item(self, item, spider):
        if self.count == 0:
            raise DropItem("Over item found: %s" % item)
        else:
            self.count -= 1
            return item
        
        
