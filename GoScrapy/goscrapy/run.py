# -*- coding: utf-8 -*-
from spiders.deep_spider import DeepSpider
from model.config import DBSession
from model.rule import Regular

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner


db=DBSession()
rules=db.query(Regular).filter(Regular.enable==1)
for rule in rules:
    runner=CrawlerRunner()    
    spider=DeepSpider(rule)
    d=runner.crawl(spider)
    d.addBoth(lambda _:reactor.stop())
    
reactor.run()