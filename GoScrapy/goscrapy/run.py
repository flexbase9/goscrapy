# -*- coding: utf-8 -*-
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from model.config import DBSession
from model.rule import Regular
import time
import json

if __name__ == "__main__":
    db=DBSession()
    site_name=sys.argv[1]
    rule=db.query(Regular).filter(Regular.name==site_name).first()
    if rule:
        custom_setting=None
        if rule.settings:
            try:
                custom_setting=json.loads('{' + rule.settings + '}')
            except ValueError:
                custom_setting=None
        settings=get_project_settings()
        if custom_setting and isinstance(custom_setting, dict):
            for (k,v) in custom_setting.items():
                settings.set(k,v)
        settings.set("START_TIME",time.time())
        process=CrawlerProcess(settings)
        process.crawl('Deep',site_name=site_name)
        process.start()