# -*- coding: utf-8 -*-
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from model.regular import Regular
import time
import json

def run_common_crawl(site_name,spider_name='Common'):
    rule=Regular(name=site_name)
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
        process.crawl(spider_name,site_name=site_name)
        process.start()

if __name__ == "__main__":
    site_name=sys.argv[1]
    if len(sys.argv)>2:
        spider_name=sys.argv[2]
    else:
        spider_name='Common'
    run_common_crawl(site_name, spider_name)