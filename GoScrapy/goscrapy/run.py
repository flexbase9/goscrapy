# -*- coding: utf-8 -*-
from spiders.deep_spider import DeepSpider
from model.config import DBSession
from model.rule import Rule

from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings 

RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider close signal """
    log.msg("Spider closed:%s" % spider, level=log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()
        
log.start(loglevel=log.DEBUG)

settings=Settings()

settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2;Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/32.0.1667.0 Safari/537.36")
settings.set("ITEM_PIPELINES",{'pipelines.DuplicatesPipeline':200,
                               'pipelines.DatabasePipeline':400,
                               'pipelines.SaveImagesPipeline':300})
settings.set("SPIDER_MIDDLEWARES",{"scrapy.spidermiddlewares.referer.RefererMiddleware":200})


db=DBSession()
rules=db.query(Rule).filter(Rule.enable==1)
for rule in rules:
    crawler=Crawler(settings)
    spider=DeepSpider(rule)
    RUNNING_CRAWLERS.append(spider)
    crawler.signals.connect(spider_closing,signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    
reactor.run()