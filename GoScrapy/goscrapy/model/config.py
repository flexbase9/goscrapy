# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

engine = create_engine('mysql+mysqlconnector://crawl:74108520@localhost:3306/crawl')
DBSession=sessionmaker(bind=engine)
Redis=redis.StrictRedis(host='localhost')