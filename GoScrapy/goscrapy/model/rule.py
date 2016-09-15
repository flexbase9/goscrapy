# -*- coding: utf-8 -*-

from sqlalchemy import Column, String , Integer
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Rule(Base):
    __tablename__ = 'rules'
    
    id=Column(Integer,primary_key=True)
    name=Column(String)
    allow_domains = Column(String)
    start_urls=Column(String)
    next_page=Column(String)
    allow_url=Column(String)
    extract_from=Column(String)
    enable=Column(Integer)
    name_xpath=Column(String)
    description_xpath = Column(String)
    price_xpath = Column(String)
    special_xpath = Column(String)
    options_xpath = Column(String)
    main_image_link_xpath = Column(String)
    multiple_images_link_xpath = Column(String)
    category_xpath = Column(String)
    images_path = Column(String)
    download = Column(String)
    sku_xpath = Column(String)