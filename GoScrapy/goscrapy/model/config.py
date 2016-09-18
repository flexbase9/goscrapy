# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import re

engine = create_engine('mysql+mysqlconnector://crawl:74108520@localhost:3306/crawl')
DBSession=sessionmaker(bind=engine)
Redis=redis.StrictRedis(host='localhost')

def __format_xpath(string,key=None):
    string=string.replace('\;','~~~~~').replace('\:','!!!!!')
    groups={"xpath": string}
    if(True if ":" in string else False):
        groups=dict([e.split(":") for e in string.split(';')])
        for (k,v) in groups.items():
            groups[k]=v.replace('~~~~~',';').replace('!!!!!',':')
        if key:
            if groups.has_key(key):
                groups=groups[key]
            else:
                return None
    return groups

def response_output(xpath,response):
    xpath=__format_xpath(xpath)
    result=''
    if xpath.has_key('xpath'):
        response_result=response.xpath(xpath['xpath']).extract()
    elif xpath.has_key('css'):
        response_result=response.css(xpath['css']).extract() 
    elif xpath.has_key('re'):
        response_result = re.compile(xpath['re']).findall(response.body)
         
               
    if response_result:
        if xpath.has_key('strip'):
            response_result=[x.strip(" \t\n\r") for x in response_result]
        if xpath.has_key('output'):
            delimitor=','
            if  xpath.has_key('delimitor'):
                delimitor=xpath['delimitor']
            result=delimitor.join(response_result[slice(*eval(xpath['output']))])
        else:
            result=response_result[0]
    else:
        if xpath.has_key('value'):
            result=xpath['value']
    
    if not result:
        return ''
    if xpath.has_key('replace'):
        for r in xpath['replace'].replace('\=','~~~~~').replace('\,','`````').split(','):
            _replace_word=r.split('=')
            if len(_replace_word)==2:
                result=result.replace(_replace_word[0].replace('~~~~~','=').replace('`````',','), _replace_word[1].replace('~~~~~','=').replace('`````',','))
            elif len(_replace_word)==1:
                result=result.replace(_replace_word[0].replace('~~~~~','=').replace('`````',','),'')
    if xpath.has_key('path_format'):
        result=''.join([a for a in result.replace(" ","-").lower() if a.isalpha() or a.isdigit() or a=='-'])
    return result
    